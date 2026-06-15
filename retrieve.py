from sentence_transformers import SentenceTransformer
import chromadb

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("stevens_reviews")

while True:
    query = input("\nEnter a question: ")

    if query.lower() == "exit":
        break

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    print("\nTOP RESULTS\n")

    for i in range(len(results["documents"][0])):
        print("=" * 60)

        print(
            "SOURCE:",
            results["metadatas"][0][i]["source"]
        )

        if "distances" in results:
            print(
                "DISTANCE:",
                results["distances"][0][i]
            )

        print("\n")
        print(results["documents"][0][i])
        print()