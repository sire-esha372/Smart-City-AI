import os

# =========================================================
# RENDER CPU OPTIMIZATION
# =========================================================

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from pathlib import Path
from functools import lru_cache

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_PATH = (
    BASE_DIR / "rag" / "documents"
)

VECTORSTORE_PATH = (
    BASE_DIR / "rag" / "vectorstore"
)

print(
    f"Documents Path : {DOCUMENTS_PATH}"
)

print(
    f"Vectorstore Path : {VECTORSTORE_PATH}"
)


# ---------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_embeddings():

    print(
        "Loading HuggingFace embedding model..."
    )

    embeddings = HuggingFaceEmbeddings(

        model_name=(
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        ),

        model_kwargs={
            "device": "cpu"
        },

        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    print(
        "HuggingFace embedding model "
        "loaded successfully."
    )

    return embeddings


# ---------------------------------------------------------------------
# Build FAISS Database
# ---------------------------------------------------------------------

def build_vectorstore():

    print(
        "Building FAISS vector database..."
    )

    if not DOCUMENTS_PATH.exists():

        raise Exception(
            f"Documents folder not found:\n"
            f"{DOCUMENTS_PATH}"
        )

    pdf_files = list(
        DOCUMENTS_PATH.glob("*.pdf")
    )

    if len(pdf_files) == 0:

        raise Exception(
            f"No PDF files found inside:\n"
            f"{DOCUMENTS_PATH}"
        )

    documents = []

    for pdf in pdf_files:

        print(
            f"Loading PDF: {pdf.name}"
        )

        loader = PyPDFLoader(
            str(pdf)
        )

        documents.extend(
            loader.load()
        )

    print(
        f"Loaded {len(documents)} document pages."
    )

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200
    )

    docs = splitter.split_documents(
        documents
    )

    print(
        f"Created {len(docs)} text chunks."
    )

    VECTORSTORE_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        "Creating FAISS embeddings..."
    )

    vectorstore = FAISS.from_documents(
        docs,
        get_embeddings()
    )

    vectorstore.save_local(
        str(VECTORSTORE_PATH)
    )

    print(
        "FAISS database created successfully!"
    )

    return vectorstore


# ---------------------------------------------------------------------
# Load FAISS Database
# ---------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_vectorstore():

    index_file = (
        VECTORSTORE_PATH / "index.faiss"
    )

    if not index_file.exists():

        print(
            "FAISS index not found."
        )

        return build_vectorstore()

    print(
        "Loading existing FAISS database..."
    )

    vectorstore = FAISS.load_local(

        str(VECTORSTORE_PATH),

        get_embeddings(),

        allow_dangerous_deserialization=True
    )

    print(
        "FAISS database loaded successfully."
    )

    return vectorstore


# ---------------------------------------------------------------------
# Ask Question
# ---------------------------------------------------------------------

def ask_question(
    question,
    groq_api_key
):

    print(
        "Starting RAG question..."
    )

    # =====================================================
    # LOAD CACHED VECTORSTORE
    # =====================================================

    vectorstore = load_vectorstore()

    # =====================================================
    # RETRIEVE ONLY TOP 3 DOCUMENTS
    # =====================================================

    print(
        "Searching knowledge base..."
    )

    documents = (
        vectorstore.similarity_search(
            question,
            k=3
        )
    )

    print(
        f"Retrieved {len(documents)} documents."
    )

    # =====================================================
    # BUILD CONTEXT
    # =====================================================

    context_parts = []

    for document in documents:

        context_parts.append(
            document.page_content
        )

    context = "\n\n".join(
        context_parts
    )

    # =====================================================
    # GROQ
    # =====================================================

    print(
        "Calling Groq LLM..."
    )

    llm = ChatGroq(

        groq_api_key=groq_api_key,

        model="llama-3.1-8b-instant",

        temperature=0,

        max_tokens=500
    )

    # =====================================================
    # PROMPT
    # =====================================================

    prompt = f"""
You are a Smart City AI assistant.

Answer the user's question ONLY using
the provided context.

If the answer is not available in the
context, say that the information is
not available in the provided documents.

Keep the answer clear and concise.

Context:
{context}

Question:
{question}

Answer:
"""

    # =====================================================
    # GENERATE ANSWER
    # =====================================================

    response = llm.invoke(
        prompt
    )

    print(
        "Groq response received."
    )

    # =====================================================
    # RETURN ANSWER
    # =====================================================

    return response.content