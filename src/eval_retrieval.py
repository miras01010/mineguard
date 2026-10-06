import json
from search import search

def run(k=5):
    with open("evals/questions.json", encoding="utf-8") as f:
        cases = json.load(f)

    hits = 0
    for case in cases:
        results = search(case["question"], k=k)
        found = [(m["source"], m["page"]) for m in results["metadatas"][0]]
        expected = (case["source"], case["page"])

        if expected in found:
            hits += 1
            rank = found.index(expected) + 1
            print(f"PASS (rank {rank}): {case['question']}")
        else:
            print(f"FAIL: {case['question']}")
            print(f"      expected {expected}, got {found}")

    print(f"\nHit rate @{k}: {hits}/{len(cases)}")

if __name__ == "__main__":
    run()