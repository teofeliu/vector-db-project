# app/services/indexing/brute_force_index.py
import numpy as np
import os
import json
from typing import List, Tuple
from .base import VectorIndex
from ..similarity import CosineSimilarity

class BruteForceIndex(VectorIndex):
    def __init__(self, index_path: str):
        print("USING BRUTE FORCE INDEXING")
        self.index_path = index_path
        self.vector_file = os.path.join(index_path, "vectors.npy")
        self.metadata_file = os.path.join(index_path, "metadata.json")
        self.similarity = CosineSimilarity()
        self.vectors = np.array([], dtype=np.float32).reshape(0, 0)
        self.metadata = {"ids": [], "dimensions": 0}
        self.load()

    def add(self, vector: List[float], id: int) -> None:
        vector = np.array(vector, dtype=np.float32)
        if self.vectors.size == 0:
            self.metadata["dimensions"] = vector.shape[0]
            self.vectors = vector.reshape(1, -1)
        else:
            self.vectors = np.vstack([self.vectors, vector])
        self.metadata["ids"].append(id)
        self.save()

    def search(self, query: List[float], k: int) -> List[Tuple[int, float]]:
        query_vector = np.array(query, dtype=np.float32)
        print("num vectors:", len(self.vectors))
        similarities = np.array([self.similarity.calculate(query_vector, vec) for vec in self.vectors])
        sorted_indices = np.argsort(similarities)[::-1]
        top_k_indices = sorted_indices[:k]
        return [(self.metadata["ids"][i], similarities[i]) for i in top_k_indices]

    def rebuild(self, vectors: List[List[float]], ids: List[int]) -> None:
        self.vectors = np.array(vectors, dtype=np.float32)
        self.metadata["ids"] = ids
        self.metadata["dimensions"] = self.vectors.shape[1]
        self.save()

    def save(self) -> None:
        np.save(self.vector_file, self.vectors)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)

    def load(self) -> None:
        if os.path.exists(self.vector_file) and os.path.exists(self.metadata_file):
            self.vectors = np.load(self.vector_file, mmap_mode='r')
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.save()