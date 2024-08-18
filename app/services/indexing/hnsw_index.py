import numpy as np
from typing import List, Dict, Any, Tuple
from queue import PriorityQueue
import json
import os
import logging
from app.services.indexing.base import VectorIndex
from app.services.similarity import CosineSimilarity

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
            print(f"Added neighbor {neighbor_id} to node {self.id} at layer {layer}")

    def get_neighbors(self, layer: int) -> List[int]:
        return self.neighbors.get(layer, [])

class HNSWIndex(VectorIndex):
    def __init__(self, index_path: str, M: int = 16, ef_construction: int = 200, ml: int = 16):
        self.index_path = index_path
        self.M = M
        self.ef_construction = ef_construction
        self.ml = ml
        self.nodes: Dict[int, Node] = {}
        self.enter_point: int = None
        self.max_level: int = -1
        self.similarity = CosineSimilarity()
        print(f"Initializing HNSWIndex with M={M}, ef_construction={ef_construction}, ml={ml}")
        self.load()

    def add(self, vector: List[float], id: int) -> None:
        print(f"Adding vector with id {id} to the index")
        vector = np.array(vector, dtype=np.float32)
        node = Node(id, vector)
        self.nodes[id] = node
        
        if self.enter_point is None:
            print(f"First node added. Setting enter_point to {id}")
            self.enter_point = id
            self.max_level = self.ml
            for layer in range(self.ml + 1):
                node.neighbors[layer] = []
        else:
            level = self._random_level()
            print(f"Generated random level {level} for node {id}")
            if level > self.max_level:
                print(f"New max level: {level}. Updating enter_point to {id}")
                self.max_level = level
                self.enter_point = id
            self._insert_node(node, level)
        self.save()

    def search(self, query: List[float], k: int) -> List[Tuple[int, float]]:
        print(f"Searching for {k} nearest neighbors")
        query = np.array(query, dtype=np.float32)
        if self.enter_point is None:
            print("Index is empty. Returning empty result.")
            return []

        enter_point = self.nodes[self.enter_point]
        current_layer = self.max_level
        current_nearest = enter_point

        while current_layer > 0:
            print(f"Searching at layer {current_layer}")
            changed = True
            while changed:
                changed = False
                for neighbor_id in current_nearest.get_neighbors(current_layer):
                    neighbor = self.nodes[neighbor_id]
                    if self.similarity.calculate(query, neighbor.vector) > self.similarity.calculate(query, current_nearest.vector):
                        current_nearest = neighbor
                        changed = True
                        print(f"Found better neighbor: {neighbor.id} at layer {current_layer}")
            current_layer -= 1

        candidates = self._search_layer(current_nearest, query, 0, self.ef_construction)

        results = []
        for node in candidates[:k]:
            similarity = self.similarity.calculate(query, node.vector)
            results.append((node.id, similarity))

        print(f"Search completed. Found {len(results)} results.")
        return sorted(results, key=lambda x: x[1], reverse=True)

    def rebuild(self, vectors: List[List[float]], ids: List[int]) -> None:
        print(f"Rebuilding index with {len(vectors)} vectors")
        self.nodes.clear()
        self.enter_point = None
        self.max_level = -1
        for vector, id in zip(vectors, ids):
            self.add(vector, id)
        print("Index rebuild completed")

    def save(self) -> None:
        print(f"Saving index to {self.index_path}")
        data = {
            "enter_point": self.enter_point,
            "max_level": self.max_level,
            "nodes": {
                str(id): {
                    "vector": node.vector.tolist(),
                    "neighbors": node.neighbors
                } for id, node in self.nodes.items()
            }
        }
        with open(os.path.join(self.index_path, "hnsw_index.json"), "w") as f:
            json.dump(data, f)
        print("Index saved successfully")

    def load(self) -> None:
        index_file = os.path.join(self.index_path, "hnsw_index.json")
        if os.path.exists(index_file):
            print(f"Loading index from {index_file}")
            with open(index_file, "r") as f:
                data = json.load(f)
            self.enter_point = data["enter_point"]
            self.max_level = data["max_level"]
            self.nodes = {
                int(id): Node(
                    int(id),
                    np.array(node_data["vector"], dtype=np.float32)
                ) for id, node_data in data["nodes"].items()
            }
            for id, node_data in data["nodes"].items():
                self.nodes[int(id)].neighbors = {int(layer): neighbors for layer, neighbors in node_data["neighbors"].items()}
            print(f"Loaded index with {len(self.nodes)} nodes")
        else:
            print(f"No existing index found at {index_file}")

    def _random_level(self) -> int:
        return min(int(-np.log(np.random.uniform()) * self.M), 
                int(np.log2(len(self.nodes) + 1)))

    def _insert_node(self, node: Node, level: int) -> None:
        print(f"Inserting node {node.id} at level {level}")
        enter_point = self.nodes[self.enter_point]
        
        for l in range(min(self.max_level, level), -1, -1):
            print(f"Inserting at layer {l}")
            neighbors = self._search_layer(enter_point, node.vector, l, self.ef_construction)
            neighbors = self._select_neighbors(node, neighbors, self.M, l)
            
            for neighbor in neighbors:
                node.add_neighbor(l, neighbor.id)
                neighbor.add_neighbor(l, node.id)
            
            if neighbors:
                enter_point = neighbors[0]
        print(f"Node {node.id} inserted successfully")

    def _search_layer(self, entry_point: Node, query: np.ndarray, layer: int, ef: int) -> List[Node]:
        print(f"Searching layer {layer} with ef={ef}")
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
            
            for neighbor_id in current.get_neighbors(layer):
                if neighbor_id not in visited:
                    neighbor = self.nodes[neighbor_id]
                    visited.add(neighbor_id)
                    similarity = self.similarity.calculate(neighbor.vector, query)
                    if similarity > furthest_similarity or results.qsize() < ef:
                        candidates.put((-similarity, neighbor))
                        results.put((similarity, neighbor))
                        if results.qsize() > ef:
                            results.get()
        
        print(f"Layer search completed. Found {results.qsize()} candidates")
        return [node for _, node in sorted(results.queue, key=lambda x: -x[0])]

    def _select_neighbors(self, node: Node, candidates: List[Node], M: int, layer: int) -> List[Node]:
        selected = sorted(candidates, key=lambda x: self.similarity.calculate(node.vector, x.vector), reverse=True)[:M]
        print(f"Selected {len(selected)} neighbors for node {node.id} at layer {layer}")
        return selected