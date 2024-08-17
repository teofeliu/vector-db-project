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
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)

    def search(self, query: List[float], k: int) -> List[Tuple[int, float]]:
        query_vector = np.array(query, dtype=np.float32)
        similarities = np.array([self.cosine_similarity(query_vector, vec) for vec in self.vectors])
        nearest_indices = np.argsort(similarities)[-k:][::-1]
        return [(self.metadata["ids"][i], similarities[i]) for i in nearest_indices]

    def rebuild(self, vectors: List[List[float]], ids: List[int]):
        self.vectors = np.array(vectors, dtype=np.float32)
        self.metadata["ids"] = ids
        self.metadata["dimensions"] = self.vectors.shape[1]
        self.save_index()