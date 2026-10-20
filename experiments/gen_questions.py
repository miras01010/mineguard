import sys, json, random
sys.path.insert(0, "src")
from search import collection
from answer import client

N = 20
random.seed(42)

PROMPT = """Below is a passage from Indian mining law.
Write ONE short question that a mine worker or mining student might ask in casual words,
which this passage clearly answers. Do not copy phrases from the passage.
If the passage has no clear rule or fact to ask about, reply exactly: SKIP"""

data = collection.get()
indices = random.sample(range(len(data["ids"])), N)

candidates = []
for i in indices:
    text, meta = data["documents"][i], data["metadatas"][i]
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": PROMPT},
                  {"role": "user", "content": text}],
        temperature=0,
    )
    question = (response.choices[0].message.content or "").strip()
    if not question or question == "SKIP":
        continue
    print(f"[{meta['source']}, p.{meta['page']}] {question}")
    candidates.append({
        "question": question,
        "answers": [{"source": meta["source"], "pages": [meta["page"]]}],
    })

with open("evals/synthetic_candidates.json", "w", encoding="utf-8") as f:
    json.dump(candidates, f, indent=2, ensure_ascii=False)
print(f"\nSaved {len(candidates)} candidates")