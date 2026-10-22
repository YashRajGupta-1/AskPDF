Phase 0 done — nice. Here's a README you can paste straight in. It's a v1; you'll expand it in Phase 8 with eval scores and the architecture diagram.
```markdown
# RAG PDF Q&A + Resume Analyzer

Ask questions about any PDF and get answers with page-level citations — plus a resume analyzer mode that scores resumes against job descriptions.

## What it does

- Upload a PDF → ask questions in plain English → get answers citing exact pages
- **Resume Analyzer mode:** upload a resume + job description → get a structured skills-match report (score, strengths, gaps, one-line advice)
- Says "I don't know" when the answer isn't in the document — no hallucinations

## Tech stack

Python, FastAPI, PyMuPDF, sentence-transformers (`all-MiniLM-L6-v2`), ChromaDB, Groq (LLM API)

Built **without LangChain** — every pipeline step (extract → chunk → embed → retrieve → generate) is hand-rolled.

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file with your free Groq key:
```
GROQ_API_KEY=gsk_your_key_here
```

Run:
```bash
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs` for the interactive API.

## Project structure

```
app/          # FastAPI server
pipeline/     # RAG engine: ingest → chunk → embed → store → retrieve
eval/         # Evaluation harness (hand-written Q&A set)
```

## Roadmap

- [x] Phase 0 — Project setup
- [ ] Phase 1 — PDF text extraction (page-aware)
- [ ] Phase 2 — Chunking with overlap + metadata
- [ ] Phase 3 — Embeddings
- [ ] Phase 4 — ChromaDB vector store
- [ ] Phase 5 — Retrieval (top-k)
- [ ] Phase 6 — Grounded generation with citations
- [ ] Phase 7 — API + minimal UI
- [ ] Phase 8 — Eval harness, reranker, hybrid search
- [ ] Resume Analyzer mode
```
Paste it, save, and commit if you're using git. Tomorrow we start *Phase 1 — ripping text out of PDFs with PyMuPDF*. For that you'll need a test PDF — grab any small one (5–10 pages, e.g. your own resume or a short article). Real text PDF, not a scanned image.