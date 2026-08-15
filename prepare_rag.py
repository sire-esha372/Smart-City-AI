import json
import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

PDF_PATH = (
    BASE_DIR
    / "backend"
    / "app"
    / "rag"
    / "documents"
    / "Smart_Cities.pdf.pdf"
)

OUTPUT_PATH = (
    BASE_DIR
    / "backend"
    / "app"
    / "rag"
    / "rag_chunks.json"
)


# =========================================================
# CHECK PDF
# =========================================================

if not PDF_PATH.exists():

    raise FileNotFoundError(
        f"PDF not found:\n{PDF_PATH}"
    )


print("=" * 60)
print("Preparing Smart City RAG document")
print("=" * 60)

print(f"PDF: {PDF_PATH}")
print(f"Output: {OUTPUT_PATH}")


# =========================================================
# LOAD PDF
# =========================================================

print("\nLoading PDF...")

loader = PyPDFLoader(
    str(PDF_PATH)
)

pages = loader.load()

print(
    f"Loaded {len(pages)} pages."
)


# =========================================================
# CREATE CHUNKS
# =========================================================

chunks = []

for page in pages:

    text = page.page_content.strip()

    if not text:
        continue

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


print(
    f"Created {len(chunks)} chunks."
)


# =========================================================
# SAVE JSON
# =========================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        chunks,
        file,
        ensure_ascii=False,
        indent=2
    )


print("\nRAG cache created successfully.")

print(
    f"Saved to:\n{OUTPUT_PATH}"
)

print("=" * 60)