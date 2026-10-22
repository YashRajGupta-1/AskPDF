def chunk_pages(pages, size=500, overlap=60):
    """Split page dicts into overlapping word-chunks, each tagged with its page."""
    chunks = []
    for p in pages:
        words = p["text"].split()
        step = size - overlap  # slide forward by 440 each time, so 60 words repeat
        for i in range(0, len(words), step):
            piece = " ".join(words[i:i + size])
            if len(piece.split()) < 30:
                continue  # drop scraps: headers, footers, orphan lines
            chunks.append({
                "text": piece,
                "page": p["page"],      # traceability → citations later
                "chunk_id": len(chunks), # unique id → vector DB key later
            })
    return chunks