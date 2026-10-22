from pipeline.ingest import extract_pages

pages = extract_pages("test.pdf")
print(f"Extracted {len(pages)} pages with text")
print(f"Pages: {[p['page'] for p in pages]}")
print("--- Page 1 preview ---")
print(pages[0]["text"][:400])