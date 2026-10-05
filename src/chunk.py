from load_pdfs import load_all

CHUNK_WORDS = 200
OVERLAP_WORDS = 40

def chunk_page(page):
    words = page["text"].split()
    chunks = []
    step = CHUNK_WORDS - OVERLAP_WORDS
    for start in range(0, len(words), step):
        chunk_words = words[start:start + CHUNK_WORDS]
        chunks.append({
            "source": page["source"],
            "page": page["page"],
            "text": " ".join(chunk_words),
        })
        if start + CHUNK_WORDS >= len(words):
            break
    return chunks

def chunk_all(pages):
    all_chunks = []
    for page in pages:
        all_chunks.extend(chunk_page(page))
    return all_chunks

if __name__ == "__main__":
    pages = load_all()
    chunks = chunk_all(pages)
    print(f"\n{len(pages)} pages -> {len(chunks)} chunks")
    print("\nExample chunk:\n")
    print(chunks[10])