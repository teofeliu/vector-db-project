# hnsw_index/node.py
import numpy as np
from typing import Dict, List

class Node:
    def __init__(self, id: int, vector: np.ndarray):
        self.id = id
        self.vector = vector
        self.neighbors: Dict[int, List[int]] = {}

    def add_neighbor(self, layer: int, neighbor_id: int):
        if layer not in self.neighbors:
            self.neighbors[layer] = []
        if neighbor_id not in self.neighbors[layer]:
            self.neighbors[layer].append(neighbor_id)

    def get_neighbors(self, layer: int) -> List[int]:
        return self.neighbors.get(layer, [])