import sys
sys.path.insert(0, "src")
from search import keyword_search, ID_TO_META

for q in ["What is the gas detection limit for a degree two seam?",
          "What is the gas detection limit for a degree two seams?"]:
    print("\n" + q)
    for cid in keyword_search(q, k=5):
        m = ID_TO_META[cid]
        print("  ", m["source"], m["page"])