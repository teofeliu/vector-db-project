# app/services/indexing/ivf_index.py
import numpy as np
import os
import json
from typing import List, Tuple
from collections import defaultdict
from sklearn.cluster import KMeans
from .base import VectorIndex
from ..similarity import CosineSimilarity

class IVFIndex(VectorIndex):
    def __init__(self, index_path: str, n_clusters: int = 100):
        self.index_path = index_path
        self.vector_file = os.path.join(index_path, "vectors.npy")
        self.metadata_file = os.path.join(index_path, "metadata.json")
        self.centroids_file = os.path.join(index_path, "centroids.npy")
        self.inverted_lists_file = os.path.join(index_path, "inverted_lists.json")
        self.similarity = CosineSimilarity()
        self.n_clusters = n_clusters
        print("IVF CHOSEN")
        print("n clusters:", n_clusters)
        self.vectors = np.array([], dtype=np.float32).reshape(0, 0)
        self.metadata = {"ids": [], "dimensions": 0}
        self.centroids = None
        self.inverted_lists = defaultdict(list)
        self.load()

    def add(self, vector: List[float], id: int) -> None:
        vector = np.array(vector, dtype=np.float32)
        if self.vectors.size == 0:
            self.metadata["dimensions"] = vector.shape[0]
            self.vectors = vector.reshape(1, -1)
        else:
            self.vectors = np.vstack([self.vectors, vector])
        self.metadata["ids"].append(id)
        
        # Assign the new vector to the nearest centroid
        if self.centroids is not None:
            distances = [self.similarity.calculate(vector, centroid) for centroid in self.centroids]
            nearest_centroid = np.argmax(distances)
            self.inverted_lists[nearest_centroid].append(len(self.metadata["ids"]) - 1)
        
        # Rebuild the index if we've added enough new vectors
        if len(self.metadata["ids"]) % self.n_clusters == 0:
            self._build_index()
        
        self.save()

    def search(self, query: List[float], k: int) -> List[Tuple[int, float]]:
        query_vector = np.array(query, dtype=np.float32)
        
        # Find the nearest centroids
        centroid_distances = [self.similarity.calculate(query_vector, centroid) for centroid in self.centroids]
        nearest_centroids = np.argsort(centroid_distances)[::-1][:self.n_clusters // 10]  # Search in top 10% of centroids
        
        # Search in the inverted lists of the nearest centroids
        candidates = []
        for centroid in nearest_centroids:
            candidates.extend(self.inverted_lists[centroid])
        
        # Calculate similarities for the candidates
        similarities = [(i, self.similarity.calculate(query_vector, self.vectors[i])) for i in candidates]
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k results
        top_k = similarities[:k]
        return [(self.metadata["ids"][i], sim) for i, sim in top_k]

    def rebuild(self, vectors: List[List[float]], ids: List[int]) -> None:
        self.vectors = np.array(vectors, dtype=np.float32)
        self.metadata["ids"] = ids
        self.metadata["dimensions"] = self.vectors.shape[1]
        self._build_index()
        self.save()

    def _build_index(self) -> None:
        # Perform k-means clustering
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        kmeans.fit(self.vectors)
        self.centroids = kmeans.cluster_centers_
        
        # Build inverted lists
        self.inverted_lists = defaultdict(list)
        for i, label in enumerate(kmeans.labels_):
            self.inverted_lists[label].append(i)

    def save(self) -> None:
        np.save(self.vector_file, self.vectors)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)
        if self.centroids is not None:
            np.save(self.centroids_file, self.centroids)
            with open(self.inverted_lists_file, 'w') as f:
                json.dump({k: v for k, v in self.inverted_lists.items()}, f)

    def load(self) -> None:
        if os.path.exists(self.vector_file) and os.path.exists(self.metadata_file):
            self.vectors = np.load(self.vector_file, mmap_mode='r')
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
            if os.path.exists(self.centroids_file) and os.path.exists(self.inverted_lists_file):
                self.centroids = np.load(self.centroids_file)
                with open(self.inverted_lists_file, 'r') as f:
                    self.inverted_lists = defaultdict(list, json.load(f))
            else:
                self._build_index()
        else:
            self.save()