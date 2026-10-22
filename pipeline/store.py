import chromadb

# One client per process, at module level (same reason as the embedding model).
# PersistentClient writes to disk — this is what makes data survive restarts.
client = chromadb.PersistentClient(path="./chroma_db")

def index_document(doc_id, chunks, vectors):
    """Store chunks + vectors. All four lists must be same length, same order —
    ChromaDB zips them by position."""
    col = client.get_or_create_collection(f"doc_{doc_id}")
    col.add(
        ids=[str(c["chunk_id"]) for c in chunks],   # unique key per chunk
        embeddings=[v.tolist() for v in vectors],   # numpy → plain lists (Chroma wants lists)
        documents=[c["text"] for c in chunks],       # original text, so we never re-read the PDF
        metadatas=[{"page": c["page"]} for c in chunks],  # page → citations later
    )
    return col

def get_collection(doc_id):
    return client.get_collection(f"doc_{doc_id}")