from pipeline.embed import embed
import numpy as np

v = embed(["hello world"])
print("shape:", v.shape)  # expect (1, 384)

sentences = [
    "The cat sat on the mat",
    "A feline rested on the rug",
    "Quantum computing uses qubits",
    "The dog barked loudly",
    "A kitten lay on the carpet",
]
vecs = embed(sentences)
sim = vecs @ vecs.T  # cosine similarity = dot product (vectors are normalized)
np.set_printoptions(precision=2, suppress=True)
print(sim)