from pathlib import Path
import re
import json
import random
 
DOCUMENTS_DIR = Path("document")
OUTPUT_FILE = Path("chunks.jsonl")
 
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
 
 
def load_documents():
    documents = []
 
    if not DOCUMENTS_DIR.is_dir():
        print(f"Directory not found: {DOCUMENTS_DIR.resolve()}")
        return documents
 
    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")
        documents.append({
            "source": file_path.name,
            "text": text,
        })
 
    return documents
 
 
def clean_text(text):
    # Decode entities FIRST, then collapse whitespace, so spaces
    # introduced by the replacements get normalized too.
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()
 
 
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    # Guard against an infinite loop when overlap >= chunk_size.
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
 
    chunks = []
    step = chunk_size - overlap
    start = 0
 
    while start < len(text):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += step
 
    return chunks
 
 
def main():
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")
 
    all_chunks = []
    for doc in documents:
        cleaned = clean_text(doc["text"])
        for i, chunk in enumerate(chunk_text(cleaned)):
            all_chunks.append({
                "id": f"{doc['source']}::{i}",
                "source": doc["source"],
                "text": chunk,
            })
 
    print(f"Total chunks: {len(all_chunks)}")
 
    # Build the chunk file (one JSON object per line — JSONL).
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    print(f"Wrote {len(all_chunks)} chunks to {OUTPUT_FILE.resolve()}")
 
    print("\n===== SAMPLE CHUNKS =====\n")
    samples = random.sample(all_chunks, min(5, len(all_chunks)))
    for i, chunk in enumerate(samples, start=1):
        print("=" * 60)
        print(f"Chunk {i}")
        print(f"Source: {chunk['source']}  (id: {chunk['id']})")
        print("-" * 60)
        print(chunk["text"])
        print()
 
 
if __name__ == "__main__":
    main()
