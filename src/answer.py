import os
from dotenv import load_dotenv
from groq import Groq
from search import search

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
LLM_MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are MineGuard, an assistant for Indian mining safety law.
Answer the question using ONLY the numbered passages provided.
After each fact, cite the passage number like [1] or [2].
If the passages do not contain the answer, say "I could not find this in the regulations." Do not guess."""

def build_context(results):
    blocks = []
    for i, (text, meta) in enumerate(
        zip(results["documents"][0], results["metadatas"][0]), start=1
    ):
        blocks.append(f"[{i}] ({meta['source']}, page {meta['page']})\n{text}")
    return "\n\n".join(blocks)

def answer(question, k=5):
    results = search(question, k=k)
    context = build_context(results)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Passages:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0,
    )
    return response.choices[0].message.content, results

if __name__ == "__main__":
    question = input("Ask a question: ")
    reply, results = answer(question)
    print("\n" + reply)
    print("\nSources:")
    for i, meta in enumerate(results["metadatas"][0], start=1):
        print(f"  [{i}] {meta['source']}, page {meta['page']}")