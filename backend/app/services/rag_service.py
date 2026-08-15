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

DOCUMENTS_PATH = BASE_DIR / "rag" / "documents"

print(f"Documents Path: {DOCUMENTS_PATH}")


# =========================================================
# CACHES
# =========================================================

documents_cache = None
retrieval_index = None


# =========================================================
# LOAD AND PREPARE DOCUMENTS
# =========================================================

def load_documents():

    global documents_cache
    global retrieval_index

    # Already loaded
    if documents_cache is not None:

        return documents_cache

    print("Loading Smart City PDF...")

    if not DOCUMENTS_PATH.exists():

        raise Exception(
            f"Documents folder not found:\n{DOCUMENTS_PATH}"
        )

    pdf_files = list(
        DOCUMENTS_PATH.glob("*.pdf")
    )

    if not pdf_files:

        raise Exception(
            f"No PDF files found inside:\n{DOCUMENTS_PATH}"
        )

    chunks = []

    # =====================================================
    # LOAD PDFS
    # =====================================================

    for pdf in pdf_files:

        print(f"Loading PDF: {pdf.name}")

        loader = PyPDFLoader(
            str(pdf)
        )

        pages = loader.load()

        for page in pages:

            text = page.page_content.strip()

            if not text:
                continue

            # ---------------------------------------------
            # Split paragraphs
            # ---------------------------------------------

            paragraphs = re.split(
                r"\n\s*\n",
                text
            )

            for paragraph in paragraphs:

                paragraph = paragraph.strip()

                if not paragraph:
                    continue

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
                        chunks.append(chunk)

    # =====================================================
    # CACHE DOCUMENTS
    # =====================================================

    documents_cache = chunks

    print(
        f"Loaded {len(documents_cache)} "
        f"document chunks."
    )

    # =====================================================
    # BUILD RETRIEVAL INDEX ONCE
    # =====================================================

    print("Building RAG retrieval index...")

    retrieval_index = []

    for document in documents_cache:

        document_lower = document.lower()

        document_words = set(
            re.findall(
                r"\b[a-zA-Z]{3,}\b",
                document_lower
            )
        )

        retrieval_index.append(
            (
                document,
                document_lower,
                document_words
            )
        )

    print("RAG retrieval index ready.")

    return documents_cache


# =========================================================
# RETRIEVE DOCUMENTS
# =========================================================

def retrieve_documents(
    question,
    top_k=3
):

    global retrieval_index

    # Make sure documents/index are loaded
    load_documents()

    if not retrieval_index:

        return []

    # =====================================================
    # QUESTION WORDS
    # =====================================================

    question_lower = (
        question.lower().strip()
    )

    question_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            question_lower
        )
    )

    # =====================================================
    # SCORE DOCUMENTS
    # =====================================================

    scored_documents = []

    for (
        document,
        document_lower,
        document_words
    ) in retrieval_index:

        overlap = (
            question_words
            & document_words
        )

        score = len(overlap)

        # Exact phrase match
        if question_lower in document_lower:

            score += 10

        if score > 0:

            scored_documents.append(
                (
                    score,
                    document
                )
            )

    # =====================================================
    # SORT BY RELEVANCE
    # =====================================================

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    selected = [
        document
        for score, document
        in scored_documents[:top_k]
    ]

    # =====================================================
    # FALLBACK
    # =====================================================

    if not selected:

        selected = documents_cache[:top_k]

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

    print("=" * 60)
    print("Starting Smart City RAG...")
    print("=" * 60)

    # =====================================================
    # RETRIEVE CONTEXT
    # =====================================================

    retrieved_documents = retrieve_documents(
        question,
        top_k=3
    )

    context = "\n\n".join(
        retrieved_documents
    )

    print(
        "Retrieved context successfully."
    )

    # =====================================================
    # GROQ
    # =====================================================

    print("Calling Groq LLM...")

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

    print("Groq response received.")

    # =====================================================
    # RETURN
    # =====================================================

    return response.content