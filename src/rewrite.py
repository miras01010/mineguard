import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
REWRITE_MODEL = "openai/gpt-oss-20b"

REWRITE_PROMPT = """You turn questions about Indian mining safety law into short search queries.
Rules:
- Keep the user's key terms; only add the formal legal term alongside them if it differs.
- Translate any Hindi or Hinglish into English.
- Do NOT add phrases like "under Indian law", "in mining operations" or "regulations".
- Maximum 15 words. Return only the query, with no explanation."""

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