import chromadb
from sentence_transformers import SentenceTransformer
from load_pdfs import load_all
from chunk import chunk_all

EMBED_MODEL = "all-MiniLM-L6-v2"
DB_PATH = "db"
COLLECTION = "regulations"

def build_index():
    chunks = chunk_all(load_all())
    texts = [c["text"] for c in chunks]

    model = SentenceTransformer(EMBED_MODEL)
    embeddings = model.encode(texts, show_progress_bar=True)

    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION, metadata={"hnsw:space": "cosine"}
    )

    collection.add(
        ids=[f"chunk-{i}" for i in range(len(chunks))],
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": c["source"], "page": c["page"]} for c in chunks],
    )
    print(f"\nIndexed {collection.count()} chunks into '{DB_PATH}/'")

if __name__ == "__main__":
    build_index()