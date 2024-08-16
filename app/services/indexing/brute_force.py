# app/services/indexing/brute_force.py
from typing import List, Tuple, Callable
import numpy as np

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return np.linalg.norm(a - b)

class BruteForceIndex:
    def __init__(self, distance_func: Callable[[np.ndarray, np.ndarray], float] = euclidean_distance):
        self.vectors: List[np.ndarray] = []
        self.ids: List[int] = []
        self.distance_func = distance_func

    def add(self, vector: List[float], id: int) -> None:
        self.vectors.append(np.array(vector))
        self.ids.append(id)

    def search(self, query: List[float], k: int) -> List[Tuple[int, float]]:
        query_vector = np.array(query)
        distances = [self.distance_func(v, query_vector) for v in self.vectors]
        indexed_distances = list(enumerate(distances))
        indexed_distances.sort(key=lambda x: x[1])
        result = []

        for i in range(min(k, len(self.ids))):
            index, distance = indexed_distances[i]
            result.append((self.ids[index], distance))
        return result

    def __len__(self) -> int:
        return len(self.ids)