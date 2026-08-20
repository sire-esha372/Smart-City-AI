import os
import re
import json
from pathlib import Path

from langchain_groq import ChatGroq


# =========================================================
# RENDER MEMORY OPTIMIZATION
# =========================================================

os.environ["TOKENIZERS_PARALLELISM"] = "false"


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAG_CACHE_PATH = (
    BASE_DIR
    / "rag"
    / "rag_chunks.json"
)

print(
    f"RAG Cache Path: {RAG_CACHE_PATH}"
)


# =========================================================
# CACHES
# =========================================================

documents_cache = None
retrieval_index = None


# =========================================================
# LOAD PREPROCESSED RAG DOCUMENTS
# =========================================================

def load_documents():

    global documents_cache
    global retrieval_index

    # -----------------------------------------------------
    # Already loaded
    # -----------------------------------------------------

    if documents_cache is not None:

        return documents_cache

    print(
        "Loading preprocessed RAG cache..."
    )

    # -----------------------------------------------------
    # Check cache file
    # -----------------------------------------------------

    if not RAG_CACHE_PATH.exists():

        raise Exception(
            f"RAG cache not found:\n"
            f"{RAG_CACHE_PATH}"
        )

    # -----------------------------------------------------
    # Load JSON
    # -----------------------------------------------------

    with open(
        RAG_CACHE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        documents_cache = json.load(
            file
        )

    print(
        f"Loaded {len(documents_cache)} "
        f"preprocessed document chunks."
    )

    # =====================================================
    # BUILD RETRIEVAL INDEX ONCE
    # =====================================================

    print(
        "Building RAG retrieval index..."
    )

    retrieval_index = []

    for document in documents_cache:

        document_lower = (
            document.lower()
        )

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

    print(
        "RAG retrieval index ready."
    )

    return documents_cache


# =========================================================
# RETRIEVE DOCUMENTS
# =========================================================

def retrieve_documents(
    question,
    top_k=3
):

    global retrieval_index

    # -----------------------------------------------------
    # Make sure documents are loaded
    # -----------------------------------------------------

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

        # -------------------------------------------------
        # Keyword overlap
        # -------------------------------------------------

        overlap = (
            question_words
            & document_words
        )

        score = len(
            overlap
        )

        # -------------------------------------------------
        # Exact phrase match
        # -------------------------------------------------

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
    # SORT BY SCORE
    # =====================================================

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    # =====================================================
    # SELECT TOP DOCUMENTS
    # =====================================================

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
    print(
        "Starting Smart City RAG..."
    )
    print("=" * 60)

    # =====================================================
    # RETRIEVE CONTEXT
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

    print(
        "Retrieved context successfully."
    )

    # =====================================================
    # GROQ
    # =====================================================

    print(
        "Calling Groq LLM..."
    )

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model="openai/gpt-oss-20b",
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