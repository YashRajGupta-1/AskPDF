read it — HeroBrine's style adds: centered header with shields.io badges, a named problem ("Commitment Gap") with bolded pain points, concrete input→output examples, and a screenshots/demo section. merging both styles into the AskPDF README:

IMG.SHIELDS.IO

Python-3776AB

](https://www.python.org/)
[

IMG.SHIELDS.IO

FastAPI-009688

](https://fastapi.tiangolo.com/)
[

IMG.SHIELDS.IO

ChromaDB-2E86C1

](https://www.trychroma.com/)
[

IMG.SHIELDS.IO

Groq-F55036

](https://groq.com/)
[

IMG.SHIELDS.IO

PyMuPDF-4B8BBE

](https://pymupdf.readthedocs.io/)

The Problem: The "Trust Gap" in Document Q&A

LLMs are fluent but untrustworthy with your documents:

Hallucinated answers: ask about a PDF and the model invents facts with total confidence — there is no link between its words and your file.
No source traceability: even when the answer is right, you can't check where it came from. No page, no passage, no proof.
Manual search doesn't scale: Ctrl+F across a 50-page PDF for every question is slow, and keyword search misses paraphrases entirely.

What's needed: a system where every answer is retrieved from the document first and generated only from what was retrieved — with citations you can verify and an honest "I don't know" when the document doesn't contain the answer.

Overview

AskPDF implements the full RAG loop by hand — no LangChain, no black boxes. A PDF goes in; grounded, cited answers come out.

🎯 Project Goals
1. No frameworks, no magic

Every stage is explicit code (pipeline/ingest.py, chunk.py, embed.py, store.py, retrieve.py, generate.py). If you can't whiteboard a layer, you don't get to keep it.

2. Citations or it didn't happen

Every chunk carries its page number from extraction to answer. Responses cite pages like [1], [2] — traceable back to the source PDF.

3. Anti-hallucination by construction

The generation prompt is strict: answer only from the retrieved context, output exactly I don't know otherwise. Verified with out-of-context probes.

4. Async ingestion API

Uploads process in the background — the API never blocks on embedding a 50-page PDF. Clients poll a processing / ready / error status.

5. Measured, not vibes-based

Retrieval is scored on a fixed question set: 6/7 queries return the correct chunk at rank 1–2. Chunk size, overlap, and k are judged against this number.

🧠 Architecture

Ingestion details:

Extract — PyMuPDF, one rule: never lose the page number. Scanned/image PDFs fail loudly (OCR out of scope).
Chunk — overlapping windows keep context across boundaries; each chunk tagged {page, chunk_id} for traceability.
Embed — model loaded once; L2 normalization makes cosine similarity a plain dot product.
Store — ChromaDB reports squared L2 distance, so reported = 2 − 2·cos θ.

Query details:

The question is embedded with the same model; retrieval returns {text, page, score} per chunk.
The prompt packs the chunks + strict grounding rules; the model cites or abstains.
✨ Core Features
Grounded Q&A with citations

Becomes:

Honest abstention

The document doesn't contain the answer, so the system says so — instead of inventing one.

Async document ingestion

Uploads return immediately; embedding runs in the background. Poll GET /documents/{id}/status until ready, then ask.

📊 Retrieval Quality

Evaluated on a multi-page assignment PDF, 7 questions:

#	Question topic	Correct chunk rank
1	Five themes	2
2	Environmental factors	1
3	Government programs	5
4	Root causes	1
5	Beyond goals 4 & 5	1
6	Strategies	1–4
7	2015 / MDGs	1

6/7 at rank 1–2. Q3 is the honest weak spot: broad topics retrieve well, narrow aspects can sink — the roadmap is an eval harness to track this properly.

🔌 API
Method	Endpoint	Description
POST	/documents	Upload a PDF → background ingestion starts
GET	/documents/{id}/status	processing / ready / error
POST	/ask	{doc_id, question} → grounded answer + citations

A single-page UI is served at /.

🖼️ Screenshots
Image not found
🛠️ Run it

Open http://localhost:8000, upload a PDF, and ask away.