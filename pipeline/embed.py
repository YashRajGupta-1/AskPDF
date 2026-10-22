from sentence_transformers import SentenceTransformer
import numpy as np

# Loaded once when the module is imported — never inside a function.
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(texts):
    """List of strings → numpy array of shape (len(texts), 384)."""
    vecs = model.encode(texts, batch_size=32, normalize_embeddings=True)
    return np.array(vecs, dtype=np.float32)