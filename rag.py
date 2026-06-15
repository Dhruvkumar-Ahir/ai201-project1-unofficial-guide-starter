from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Groq client
client_groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB
client_db = chromadb.PersistentClient(path="chroma_db")

collection = client_db.get_collection(
    "stevens_reviews"
)

while True:
    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    context = ""

    sources = set()

    for i in range(len(results["documents"][0])):
        context += (
            results["documents"][0][i]
            + "\n\n"
        )

        sources.add(
            results["metadatas"][0][i]["source"]
        )

    prompt = f"""
You are a Stevens Institute of Technology
student guide assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context,
say:
'I don't have enough information in the documents provided.'

Context:
{context}

Question:
{question}
"""

    response = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nANSWER\n")
    print(
        response.choices[0].message.content
    )

    print("\nSOURCES")
    for source in sources:
        print("-", source)