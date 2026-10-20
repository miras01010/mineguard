import json
from search import search_multi, hybrid_search
from rewrite import rewrite_query

def run(k=5, rewrite=False, hybrid=False, path="evals/questions.json"):
    with open(path, encoding="utf-8") as f:
        cases = json.load(f)
    rr_total=0
    hits = 0
    for case in cases:
        queries = [case["question"]]
        if rewrite:
            rewritten = rewrite_query(case["question"])
            if rewritten:
                queries.append(rewritten)
                print(f"  → {rewritten}")
        if hybrid:
            found = [(m["source"], m["page"]) for cid, m in hybrid_search(case["question"], k=k)]
        else:
            ranked = search_multi(queries, k=k)
            found = [(meta["source"], meta["page"]) for text, meta, dist in ranked]
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
    for hybrid in (False, True):
        print(f"\n##### hybrid={hybrid} #####")
        print("=== Hand-written ===")
        run(hybrid=hybrid)
        print("\n=== Synthetic ===")
        run(path="evals/synthetic.json", hybrid=hybrid)