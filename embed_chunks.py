from sentence_transformers import SentenceTransformer
import chromadb
import json

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")

# Create or get collection
collection = client.get_or_create_collection(
    name="stevens_reviews"
)

# Load chunks from chunks.jsonl
chunks = []

with open("chunks.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        chunks.append(json.loads(line))

print(f"Loaded {len(chunks)} chunks")

# Create embeddings
texts = [chunk["text"] for chunk in chunks]

embeddings = model.encode(texts).tolist()

# Store in ChromaDB
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[str(i)],
        documents=[chunk["text"]],
        embeddings=[embeddings[i]],
        metadatas=[{
            "source": chunk["source"]
        }]
    )

print(f"Stored {len(chunks)} chunks in ChromaDB")