import os
import re
import uuid
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from pipeline.ingest import extract_pages
from pipeline.chunk import chunk_pages
from pipeline.embed import embed
from pipeline.store import index_document
from pipeline.retrieve import retrieve
from pipeline.generate import build_prompt, ask_llm

app = FastAPI(title="RAG PDF QA")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

status = {}  # doc_id -> "processing" | "ready" | "error: ..."

class AskRequest(BaseModel):
    doc_id: str
    question: str

@app.get("/health")
def health():
    return {"ok": True}

def _slug(filename: str) -> str:
    stem = os.path.splitext(filename)[0]
    clean = re.sub(r"[^a-zA-Z0-9_-]+", "-", stem).strip("-") or "doc"
    return f"{clean}-{uuid.uuid4().hex[:6]}"  # readable + collision-proof

def ingest_document(doc_id: str, path: str):
    try:
        pages = extract_pages(path)
        chunks = chunk_pages(pages)
        vectors = embed([c["text"] for c in chunks])
        index_document(doc_id, chunks, vectors)
        status[doc_id] = "ready"
    except Exception as e:
        status[doc_id] = f"error: {e}"  # surfaces in the UI instead of vanishing

@app.post("/documents")
def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    doc_id = _slug(file.filename)
    path = os.path.join(UPLOAD_DIR, doc_id + ".pdf")
    with open(path, "wb") as f:
        f.write(file.file.read())
    status[doc_id] = "processing"
    background_tasks.add_task(ingest_document, doc_id, path)
    return {"doc_id": doc_id, "status": "processing"}

@app.get("/documents/{doc_id}/status")
def document_status(doc_id: str):
    if doc_id not in status:
        raise HTTPException(404, "unknown document")
    return {"doc_id": doc_id, "status": status[doc_id]}

@app.post("/ask")
def ask(req: AskRequest):
    st = status.get(req.doc_id)
    if st != "ready":
        raise HTTPException(400, f"document not ready (status: {st})")
    chunks = retrieve(req.doc_id, req.question, k=8)
    answer = ask_llm(build_prompt(req.question, chunks))
    return {
        "answer": answer,
        "citations": [
            {"n": i + 1, "page": c["page"], "snippet": c["text"][:200]}
            for i, c in enumerate(chunks)
        ],
    }

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")