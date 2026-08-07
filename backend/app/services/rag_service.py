from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_PATH = BASE_DIR / "rag" / "documents"
VECTORSTORE_PATH = BASE_DIR / "rag" / "vectorstore"


print(f"Documents Path : {DOCUMENTS_PATH}")
print(f"Vectorstore Path : {VECTORSTORE_PATH}")


# ---------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------------------------------------------------------------
# Build FAISS Database
# ---------------------------------------------------------------------

def build_vectorstore():

    print("Building FAISS vector database...")

    if not DOCUMENTS_PATH.exists():
        raise Exception(f"Documents folder not found:\n{DOCUMENTS_PATH}")

    pdf_files = list(DOCUMENTS_PATH.glob("*.pdf"))

    if len(pdf_files) == 0:
        raise Exception(
            f"No PDF files found inside:\n{DOCUMENTS_PATH}"
        )

    documents = []

    for pdf in pdf_files:

        print(f"Loading: {pdf.name}")

        loader = PyPDFLoader(str(pdf))

        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)

    VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)

    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    vectorstore.save_local(str(VECTORSTORE_PATH))

    print("FAISS database created successfully!")

    return vectorstore


# ---------------------------------------------------------------------
# Load FAISS Database
# ---------------------------------------------------------------------

def load_vectorstore():

    index_file = VECTORSTORE_PATH / "index.faiss"

    if not index_file.exists():

        return build_vectorstore()

    print("Loading existing FAISS database...")

    return FAISS.load_local(
        str(VECTORSTORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )


# ---------------------------------------------------------------------
# Ask Question
# ---------------------------------------------------------------------

def ask_question(question, groq_api_key):

    vectorstore = load_vectorstore()

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model="llama-3.1-8b-instant"
    )

    prompt = ChatPromptTemplate.from_template(
        """
Answer the user's question ONLY using the context below.

Context:
{context}

Question:
{input}

Answer:
"""
    )

    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    retrieval_chain = create_retrieval_chain(
        vectorstore.as_retriever(),
        document_chain
    )

    response = retrieval_chain.invoke(
        {
            "input": question
        }
    )

    return response["answer"]