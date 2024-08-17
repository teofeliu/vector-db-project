import numpy as np
import os
import json
from typing import List, Tuple

class DiskBasedVectorIndex:
    def __init__(self, index_path: str):
        self.index_path = index_path
        self.vector_file = os.path.join(index_path, "vectors.npy")
        self.metadata_file = os.path.join(index_path, "metadata.json")
        self.load_or_create_index()

    def load_or_create_index(self):
        if os.path.exists(self.vector_file) and os.path.exists(self.metadata_file):
            self.vectors = np.load(self.vector_file, mmap_mode='r')
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.vectors = np.array([], dtype=np.float32).reshape(0, 0)
            self.metadata = {"ids": [], "dimensions": 0}
            self.save_index()

    def save_index(self):
        np.save(self.vector_file, self.vectors)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)

    def add(self, vector: List[float], id: int):
        vector = np.array(vector, dtype=np.float32)
        if self.vectors.size == 0:
            self.metadata["dimensions"] = vector.shape[0]
            self.vectors = vector.reshape(1, -1)
        else:
            self.vectors = np.vstack([self.vectors, vector])
        self.metadata["ids"].append(id)
        self.save_index()

    def search(self, query: List[float], k: int) -> List[Tuple[int, float]]:
        query_vector = np.array(query, dtype=np.float32)
        distances = np.linalg.norm(self.vectors - query_vector, axis=1)
        nearest_indices = np.argsort(distances)[:k]
        return [(self.metadata["ids"][i], distances[i]) for i in nearest_indices]

    def rebuild(self, vectors: List[List[float]], ids: List[int]):
        self.vectors = np.array(vectors, dtype=np.float32)
        self.metadata["ids"] = ids
        self.metadata["dimensions"] = self.vectors.shape[1]
        self.save_index()