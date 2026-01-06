import os
import faiss
import glob
from sentence_transformers import SentenceTransformer
import numpy as np

DATA_DIR = "data"
INDEX_DIR = "index"
os.makedirs(INDEX_DIR, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
sources = []

for path in glob.glob(f"{DATA_DIR}/*.md"):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        documents.append(text)
        sources.append(os.path.basename(path))

embeddings = model.encode(documents, convert_to_numpy=True)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, f"{INDEX_DIR}/faiss_index.bin")

np.save(f"{INDEX_DIR}/sources.npy", np.array(sources))
np.save(f"{INDEX_DIR}/docs.npy", np.array(documents))

print("FAISS index built successfully!")
