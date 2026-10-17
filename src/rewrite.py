import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
REWRITE_MODEL = "openai/gpt-oss-20b"

REWRITE_PROMPT = """You turn questions about Indian mining safety law into search queries.
Rewrite the question using the formal vocabulary of Indian mining regulations,
for example "shotfirer" instead of "blasting guy", or "cage" instead of "lift".
Translate any Hindi or Hinglish into English.
Return only the rewritten query, with no explanation."""

def rewrite_query(question):
    response = client.chat.completions.create(
        model=REWRITE_MODEL,
        messages=[
            {"role": "system", "content": REWRITE_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()