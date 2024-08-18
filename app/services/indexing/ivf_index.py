import numpy as np
import os
import json
from typing import List, Tuple
from collections import defaultdict
from sklearn.cluster import KMeans
from .base import VectorIndex
from ..similarity import CosineSimilarity
import logging

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
            self.metadata["dimensions"] = int(vector.shape[0])  # Convert to int
            self.vectors = vector.reshape(1, -1)
        else:
            self.vectors = np.vstack([self.vectors, vector])
        self.metadata["ids"].append(id)
        
        # Assign the new vector to the nearest centroid
        if self.centroids is not None:
            distances = [self.similarity.calculate(vector, centroid) for centroid in self.centroids]
            nearest_centroid = int(np.argmax(distances))  # Convert to int
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
            candidates.extend(self.inverted_lists[int(centroid)])  # Convert to int
        
        # Calculate similarities for the candidates
        similarities = [(int(i), self.similarity.calculate(query_vector, self.vectors[i])) for i in candidates]
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k results
        top_k = similarities[:k]
        return [(self.metadata["ids"][i], sim) for i, sim in top_k]

    def rebuild(self, vectors: List[List[float]], ids: List[int]) -> None:
        self.vectors = np.array(vectors, dtype=np.float32)
        self.metadata["ids"] = ids
        self.metadata["dimensions"] = int(self.vectors.shape[1])  # Convert to int
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
            self.inverted_lists[int(label)].append(i)  # Convert to int

    def save(self) -> None:
        np.save(self.vector_file, self.vectors)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)
        if self.centroids is not None:
            np.save(self.centroids_file, self.centroids)
            with open(self.inverted_lists_file, 'w') as f:
                # Convert keys to strings for JSON serialization
                json_inverted_lists = {str(k): v for k, v in self.inverted_lists.items()}
                json.dump(json_inverted_lists, f)

    def load(self) -> None:
        try:
            if os.path.exists(self.vector_file) and os.path.getsize(self.vector_file) > 0:
                self.vectors = np.load(self.vector_file, mmap_mode='r')
                logging.info(f"Loaded vectors, shape: {self.vectors.shape}")
            else:
                logging.warning("Vector file does not exist or is empty. Initializing empty vectors.")
                self.vectors = np.array([], dtype=np.float32).reshape(0, 0)

            if os.path.exists(self.metadata_file) and os.path.getsize(self.metadata_file) > 0:
                with open(self.metadata_file, 'r') as f:
                    file_content = f.read()
                    if file_content.strip():
                        self.metadata = json.loads(file_content)
                        logging.info(f"Loaded metadata: {self.metadata}")
                    else:
                        logging.warning("Metadata file is empty. Initializing default metadata.")
                        self.metadata = {"ids": [], "dimensions": 0}
            else:
                logging.warning("Metadata file does not exist or is empty. Initializing default metadata.")
                self.metadata = {"ids": [], "dimensions": 0}

            if os.path.exists(self.centroids_file) and os.path.getsize(self.centroids_file) > 0:
                self.centroids = np.load(self.centroids_file)
                logging.info(f"Loaded centroids, shape: {self.centroids.shape}")
            else:
                logging.warning("Centroids file does not exist or is empty. Centroids will be None.")
                self.centroids = None

            if os.path.exists(self.inverted_lists_file) and os.path.getsize(self.inverted_lists_file) > 0:
                with open(self.inverted_lists_file, 'r') as f:
                    file_content = f.read()
                    if file_content.strip():
                        json_inverted_lists = json.loads(file_content)
                        self.inverted_lists = defaultdict(list, {int(k): v for k, v in json_inverted_lists.items()})
                        logging.info(f"Loaded inverted lists, number of lists: {len(self.inverted_lists)}")
                    else:
                        logging.warning("Inverted lists file is empty. Initializing empty inverted lists.")
                        self.inverted_lists = defaultdict(list)
            else:
                logging.warning("Inverted lists file does not exist or is empty. Initializing empty inverted lists.")
                self.inverted_lists = defaultdict(list)

            if self.vectors.size > 0 and self.centroids is None:
                logging.info("Vectors exist but centroids do not. Rebuilding index.")
                self._build_index()
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {str(e)}")
            logging.error(f"Problematic file content: {file_content}")
            # Initialize with default values
            self.metadata = {"ids": [], "dimensions": 0}
            self.inverted_lists = defaultdict(list)
        except Exception as e:
            logging.error(f"Error loading index: {str(e)}")
            # Initialize with default values
            self.vectors = np.array([], dtype=np.float32).reshape(0, 0)
            self.metadata = {"ids": [], "dimensions": 0}
            self.centroids = None
            self.inverted_lists = defaultdict(list)

        logging.info("Index loading completed.")