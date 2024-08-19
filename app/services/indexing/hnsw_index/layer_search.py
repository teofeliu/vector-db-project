# hnsw_index/layer_search.py
from typing import List, Dict
import numpy as np
from queue import PriorityQueue
from .node import Node

class LayerSearch:
    def __init__(self, nodes: Dict[int, Node], similarity):
        self.nodes = nodes
        self.similarity = similarity

    def search_top_layers(self, query: np.ndarray, enter_point: Node, max_level: int) -> Node:
        current_nearest = enter_point
        for layer in range(max_level, 0, -1):
            current_nearest = self._search_layer(current_nearest, query, layer)
        return current_nearest

    def search_bottom_layer(self, entry_point: Node, query: np.ndarray, ef: int) -> List[Node]:
        visited = set()
        candidates = PriorityQueue()
        results = PriorityQueue()
        
        similarity = self.similarity.calculate(entry_point.vector, query)
        candidates.put((-similarity, entry_point))
        results.put((similarity, entry_point))
        visited.add(entry_point.id)
        
        while not candidates.empty():
            _, current = candidates.get()
            furthest_similarity, _ = results.queue[0]
            
            if self.similarity.calculate(current.vector, query) < furthest_similarity:
                break
            
            for neighbor_id in current.get_neighbors(0):
                if neighbor_id not in visited:
                    neighbor = self.nodes[neighbor_id]
                    visited.add(neighbor_id)
                    similarity = self.similarity.calculate(neighbor.vector, query)
                    if similarity > furthest_similarity or results.qsize() < ef:
                        candidates.put((-similarity, neighbor))
                        results.put((similarity, neighbor))
                        if results.qsize() > ef:
                            results.get()
        
        return [node for _, node in sorted(results.queue, key=lambda x: -x[0])]

    def _search_layer(self, entry_point: Node, query: np.ndarray, layer: int) -> Node:
        current_nearest = entry_point
        while True:
            changed = False
            for neighbor_id in current_nearest.get_neighbors(layer):
                neighbor = self.nodes[neighbor_id]
                if self.similarity.calculate(query, neighbor.vector) > self.similarity.calculate(query, current_nearest.vector):
                    current_nearest = neighbor
                    changed = True
            if not changed:
                break
        return current_nearest