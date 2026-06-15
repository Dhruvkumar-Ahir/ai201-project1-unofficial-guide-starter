import gradio as gr
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client_groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

model = SentenceTransformer("all-MiniLM-L6-v2")

client_db = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client_db.get_collection(
    "stevens_reviews"
)

def ask(question):

    query_embedding = model.encode(
        question
    ).tolist()

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
Answer using ONLY the context.

If the answer is not in the context,
say:
I don't have enough information in the documents provided.

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

    answer = response.choices[0].message.content

    return answer, "\n".join(sources)


with gr.Blocks() as demo:
    gr.Markdown(
        "# Stevens Professor Review Assistant"
    )

    question = gr.Textbox(
        label="Question"
    )

    answer = gr.Textbox(
        label="Answer",
        lines=8
    )

    sources = gr.Textbox(
        label="Sources",
        lines=4
    )

    button = gr.Button("Ask")

    button.click(
        ask,
        inputs=question,
        outputs=[answer, sources]
    )

demo.launch()