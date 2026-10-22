from pipeline.embed import embed
from pipeline.store import get_collection

def retrieve(doc_id, question, k=8):
    """Embed the question, return top-k chunks as {text, page, score} dicts."""
    qvec = embed([question])  # same model as the documents — see concept note 1
    col = get_collection(doc_id)
    res = col.query(query_embeddings=qvec.tolist(), n_results=k)
    return [
        {"text": d, "page": m["page"], "score": s}
        for d, m, s in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]