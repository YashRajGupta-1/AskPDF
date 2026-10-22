from pipeline.ingest import extract_pages
from pipeline.chunk import chunk_pages
from pipeline.embed import embed
from pipeline.store import client, index_document, get_collection

# Fresh start so re-runs don't hit duplicate-id errors
try:
    client.delete_collection("doc_test")
except Exception:
    pass

pages = extract_pages("test.pdf")
chunks = chunk_pages(pages)
vectors = embed([c["text"] for c in chunks])

index_document("test", chunks, vectors)
print(f"Indexed {len(chunks)} chunks → collection count: {get_collection('test').count()}")