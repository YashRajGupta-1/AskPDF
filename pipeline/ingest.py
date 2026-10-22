import pymupdf     # PyMuPDF

def extract_pages(path):
    """Extract text from a PDF, one dict per page: {"page": N, "text": ...}."""
    doc = pymupdf.open(path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:  # skip blank pages — empty strings become junk chunks later
            pages.append({"page": i + 1, "text": text})
    if not pages:
        raise ValueError("No extractable text — scanned PDF, needs OCR")
    return pages