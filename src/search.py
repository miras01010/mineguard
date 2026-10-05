import chromadb
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

if __name__ == "__main__":
    question = input("Ask a question: ")
    results = search(question)
    for text, meta, dist in zip(results["documents"][0],
                                results["metadatas"][0],
                                results["distances"][0]):
        print(f"\n[{meta['source']}, page {meta['page']}]  distance: {dist:.3f}")
        print(text[:300])