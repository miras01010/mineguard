from pathlib import Path
import pymupdf

RAW_DIR = Path("data/raw")

COMMON_WORDS = {"the", "of", "and", "to", "shall", "in", "be", "or", "any", "by"}

def is_english(text):
    words = text.lower().split()
    if not words:
        return False
    hits = sum(1 for w in words if w in COMMON_WORDS)
    return hits >= 2 and hits / len(words) >= 0.01

def remove_gazette_header(text):
    lines = text.splitlines()
    if lines and lines[0].strip().isdigit():
        lines = lines[1:]
    kept = []
    for line in lines:
        clean = " ".join(line.split()).upper()
        if "GAZETTE OF INDIA" in clean or clean.startswith("[PART II"):
            continue
        kept.append(line)
    return "\n".join(kept)

def load_pdf(path):
    doc = pymupdf.open(path)
    pages = []
    skipped = []
    for i, page in enumerate(doc):
        text = remove_gazette_header(page.get_text())
        if not is_english(text):
            skipped.append(i + 1)
            continue
        pages.append({"source": path.name, "page": i + 1, "text": text})
    print(f"{path.name}: kept {len(pages)}, skipped {len(skipped)}")
    if skipped:
        print(f"  skipped pages: {skipped[:20]}{' ...' if len(skipped) > 20 else ''}")
    return pages

def load_all():
    all_pages = []
    for pdf_path in sorted(RAW_DIR.glob("*.pdf")):
        pages = load_pdf(pdf_path)
        all_pages.extend(pages)
    return all_pages

if __name__ == "__main__":
    pages = load_all()
    print(f"\nTotal: {len(pages)} pages")
    