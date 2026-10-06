import os
from dotenv import load_dotenv
from groq import Groq
from search import search_with_neighbours

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
LLM_MODEL = "openai/gpt-oss-120b"

DOC_NAMES = {
    "Coal_Mines_Regulation_2017_Noti.pdf": "Coal Mines Regulations, 2017 (coal mines)",
    "Metalliferous1961.pdf": "Metalliferous Mines Regulations, 1961 (metal mines)",
    "Mines Rescue Rules, 1985.pdf": "Mines Rescue Rules, 1985",
    "MinesAct1952.pdf": "Mines Act, 1952 (all mines)",
}

SYSTEM_PROMPT = """You are MineGuard, an assistant for Indian mining safety law.
Your task: answer the user's question using the numbered passages provided.
Rules:
1. Use ONLY information from the passages. Never use outside knowledge.
2. After each fact, cite the passage number in square brackets, like [1] or [2]. Do not use any other citation format.
3. If the passages do not contain the answer, say "I could not find this in the regulations." Do not guess.
4. Be specific. Always include exact numbers, percentages, time limits and conditions from the passages, and never generalise them. Never make up numbers that are not in the passages.
5. Name the regulation each rule comes from. If the passages come from both the Coal Mines Regulations and the Metalliferous Mines Regulations, answer in separate sections headed by each regulation's name.
6. Explain the reason behind a safety rule only if the passages themselves state it.
7. Include any thresholds or conditions that decide when a rule applies, even if they appear in a different clause or sub-regulation from the rule itself. For example, if a rule applies "when gas is detected", include the limits that define detection.
"""

def build_context(chunks):
    blocks = []
    for i, (text, meta) in enumerate(chunks, start=1):
        name = DOC_NAMES.get(meta["source"], meta["source"])
        blocks.append(f"[{i}] ({name}, page {meta['page']})\n{text}")
    return "\n\n".join(blocks)

def answer(question, k=5):
    chunks = search_with_neighbours(question, k=k)
    context = build_context(chunks)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Passages:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0,
    )
    return response.choices[0].message.content, chunks

if __name__ == "__main__":
    question = input("Ask a question: ")
    reply, chunks = answer(question)
    print("\n" + reply)
    print("\nSources:")
    for i, (text, meta) in enumerate(chunks, start=1):
        print(f"  [{i}] {meta['source']}, page {meta['page']}")
    