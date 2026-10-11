import chromadb
from chunk import OVERLAP_WORDS
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "all-MiniLM-L6-v2"
DB_PATH = "db"
COLLECTION = "regulations"

model = SentenceTransformer(EMBED_MODEL)
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(COLLECTION)

def search(question, k=3):
    query_embedding = model.encode([question]).tolist()
    return collection.query(query_embeddings=query_embedding, n_results=k)

def chunk_number(chunk_id):
    return int(chunk_id.split("-")[1])

def candidate_numbers(hit_ids, total):
    candidates = set()
    for chunk_id in hit_ids:
        n = chunk_number(chunk_id)
        for m in (n - 1, n, n + 1):
            if 0<=m<total:
                candidates.add(m)
    return candidates

def search_with_neighbours(question, k=5):
    results = search(question, k=k)
    hit_ids = results["ids"][0]
    hit_numbers = [chunk_number(cid) for cid in hit_ids]

    to_fetch = candidate_numbers(hit_ids, collection.count())
    fetched = collection.get(ids=[f"chunk-{m}" for m in to_fetch])
    chunks = {
        chunk_number(cid): (text, meta)
        for cid, text, meta in zip(fetched["ids"], fetched["documents"], fetched["metadatas"])
    }

    keep = set()
    for n in hit_numbers:
        keep.add(n)
        for m in (n - 1, n + 1):
            if m in chunks and chunks[m][1]["source"]==chunks[n][1]["source"]:
                keep.add(m)

    return merge_passages(sorted(keep), chunks)

def merge_passages(numbers, chunks):
    passages = []
    for i, n in enumerate(numbers):
        text, meta = chunks[n]
        if i > 0:
            prev_meta = chunks[numbers[i - 1]][1]
        continues = i>0 and n-numbers[i-1]==1 and meta["source"]==prev_meta["source"]
        if continues:
            if meta["page"] == prev_meta["page"]:
                text = " ".join(text.split()[OVERLAP_WORDS:])
            passages[-1]["text"] += " " + text
            passages[-1]["end_page"] = meta["page"]
        else:
            passages.append({
                "source": meta["source"],
                "start_page": meta["page"],
                "end_page": meta["page"],
                "text": text,
            })
    return passages

if __name__ == "__main__":
    question = input("Ask a question: ")
    results = search(question)
    for text, meta, dist in zip(results["documents"][0],
                                results["metadatas"][0],
                                results["distances"][0]):
        print(f"\n[{meta['source']}, page {meta['page']}]  distance: {dist:.3f}")
        print(text[:300])