import os
import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq


# =========================================================
# RENDER MEMORY OPTIMIZATION
# =========================================================

os.environ["TOKENIZERS_PARALLELISM"] = "false"


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_PATH = (
    BASE_DIR / "rag" / "documents"
)

print(
    f"Documents Path : {DOCUMENTS_PATH}"
)


# =========================================================
# IN-MEMORY DOCUMENT CACHE
# =========================================================

documents = None


# =========================================================
# LOAD PDF DOCUMENT
# =========================================================

def load_documents():

    global documents

    if documents is not None:

        return documents

    print(
        "Loading Smart City PDF..."
    )

    if not DOCUMENTS_PATH.exists():

        raise Exception(
            f"Documents folder not found:\n"
            f"{DOCUMENTS_PATH}"
        )

    pdf_files = list(
        DOCUMENTS_PATH.glob("*.pdf")
    )

    if not pdf_files:

        raise Exception(
            f"No PDF files found inside:\n"
            f"{DOCUMENTS_PATH}"
        )

    all_text = []

    for pdf in pdf_files:

        print(
            f"Loading PDF: {pdf.name}"
        )

        loader = PyPDFLoader(
            str(pdf)
        )

        pages = loader.load()

        for page in pages:

            text = page.page_content.strip()

            if text:

                all_text.append(text)

    # =====================================================
    # SPLIT INTO SMALL CHUNKS
    # =====================================================

    chunks = []

    for text in all_text:

        # Split paragraphs first
        paragraphs = re.split(
            r"\n\s*\n",
            text
        )

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:

                continue

            # Keep chunks reasonably small
            words = paragraph.split()

            chunk_size = 180

            for i in range(
                0,
                len(words),
                chunk_size
            ):

                chunk = " ".join(
                    words[
                        i:i + chunk_size
                    ]
                )

                if chunk:

                    chunks.append(
                        chunk
                    )

    documents = chunks

    print(
        f"Loaded {len(documents)} "
        f"lightweight document chunks."
    )

    return documents


# =========================================================
# LIGHTWEIGHT KEYWORD RETRIEVAL
# =========================================================

def retrieve_documents(
    question,
    top_k=3
):

    docs = load_documents()

    # =====================================================
    # QUESTION WORDS
    # =====================================================

    question_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            question.lower()
        )
    )

    # =====================================================
    # SCORE EACH CHUNK
    # =====================================================

    scored_documents = []

    for document in docs:

        document_words = set(
            re.findall(
                r"\b[a-zA-Z]{3,}\b",
                document.lower()
            )
        )

        # Basic keyword overlap
        overlap = (
            question_words
            & document_words
        )

        score = len(
            overlap
        )

        # =================================================
        # EXTRA SCORE FOR EXACT QUESTION PHRASES
        # =================================================

        question_lower = (
            question.lower().strip()
        )

        document_lower = (
            document.lower()
        )

        if question_lower in document_lower:

            score += 10

        scored_documents.append(
            (
                score,
                document
            )
        )

    # =====================================================
    # SORT
    # =====================================================

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    # =====================================================
    # RETURN TOP DOCUMENTS
    # =====================================================

    selected = [
        document
        for score, document
        in scored_documents[:top_k]
        if score > 0
    ]

    # If no keyword matches, return first
    # few chunks so the LLM still has context.
    if not selected:

        selected = docs[:top_k]

    print(
        f"Retrieved {len(selected)} "
        f"document chunks."
    )

    return selected


# =========================================================
# ASK QUESTION
# =========================================================

def ask_question(
    question,
    groq_api_key
):

    print(
        "Starting lightweight RAG..."
    )

    # =====================================================
    # RETRIEVE RELEVANT CONTEXT
    # =====================================================

    retrieved_documents = (
        retrieve_documents(
            question,
            top_k=3
        )
    )

    context = "\n\n".join(
        retrieved_documents
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
the context provided below.

If the answer is not available in the
context, clearly say:

"The information is not available
in the provided government document."

Do not invent information.

Keep the answer clear and concise.

Context:
{context}

Question:
{question}

Answer:
"""

    # =====================================================
    # LLM RESPONSE
    # =====================================================

    response = llm.invoke(
        prompt
    )

    print(
        "Groq response received."
    )

    # =====================================================
    # RETURN
    # =====================================================

    return response.content