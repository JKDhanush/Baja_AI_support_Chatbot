import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("index/faiss_index.bin")

docs = np.load("index/docs.npy", allow_pickle=True)
sources = np.load("index/sources.npy", allow_pickle=True)

def retrieve(query, k=2):
    q_emb = model.encode([query])
    D, I = index.search(q_emb, k)
    return [(docs[i], sources[i]) for i in I[0]]
