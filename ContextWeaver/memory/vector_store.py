# memory/vector_store.py

import os
import faiss
import pickle
import numpy as np
from typing import List

class VectorStore:
    def __init__(self, dim: int = 1536, index_file: str = "memory/faiss_index.idx", metadata_file: str = "memory/metadata.pkl"):
        self.dim = dim
        self.index_file = index_file
        self.metadata_file = metadata_file

        # Try loading existing index
        if os.path.exists(index_file) and os.path.exists(metadata_file):
            self.index = faiss.read_index(index_file)
            with open(metadata_file, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(dim)
            self.metadata = []

    def add(self, embedding: np.ndarray, metadata: dict):
        assert embedding.shape[0] == self.dim, "Embedding size mismatch"
        self.index.add(np.array([embedding]))
        self.metadata.append(metadata)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[dict]:
        D, I = self.index.search(np.array([query_embedding]), top_k)
        return [self.metadata[i] for i in I[0] if i < len(self.metadata)]

    def save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, "wb") as f:
            pickle.dump(self.metadata, f)

