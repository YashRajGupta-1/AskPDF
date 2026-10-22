from pipeline.ingest import extract_pages
from pipeline.chunk import chunk_pages
import random

pages = extract_pages("test.pdf")
chunks = chunk_pages(pages)

print(f"{len(pages)} pages → {len(chunks)} chunks")
avg = sum(len(c["text"].split()) for c in chunks) / len(chunks)
print(f"Avg words per chunk: {avg:.0f}")

print("\n--- 3 random chunks ---")
for c in random.sample(chunks, min(3, len(chunks))):
    print(f"[chunk {c['chunk_id']}, page {c['page']}] {c['text'][:250]}...\n")