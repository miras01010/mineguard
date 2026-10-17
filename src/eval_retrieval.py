import json
from search import search
from rewrite import rewrite_query

def run(k=5, rewrite=False):
    with open("evals/questions.json", encoding="utf-8") as f:
        cases = json.load(f)
    rr_total=0
    hits = 0
    for case in cases:
        query=rewrite_query(case["question"]) if rewrite else case["question"]
        print(f"  → {query}")
        results = search(query, k=k)
        found = [(m["source"], m["page"]) for m in results["metadatas"][0]]
        expected = {(a["source"], p) for a in case["answers"] for p in a["pages"]}

        rank = None                                                   
        for i, pair in enumerate(found):
            if pair in expected:
                rank = i + 1
                break

        if rank is not None:                                          
            hits += 1
            rr_total+=1/rank
            print(f"PASS (rank {rank}): {case['question']}")
        else:
            print(f"FAIL: {case['question']}")
            print(f"      expected {expected}, got {found}")

    print(f"\nHit rate @{k}: {hits}/{len(cases)}")
    print(f"MRR: {rr_total / len(cases):.3f}")

if __name__ == "__main__":
    run()