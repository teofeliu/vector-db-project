# hnsw_index/hnsw_index.py
from typing import List, Dict, Tuple
import numpy as np
from .node import Node
from .config import HNSWConfig
from .index_io import IndexIO
from .layer_search import LayerSearch
from .node_insertion import NodeInsertion
from .utils import random_level
from app.services.similarity import CosineSimilarity

class HNSWIndex:
    def __init__(self, index_path: str, config: HNSWConfig):
        self.config = config
        self.nodes: Dict[int, Node] = {}
        self.enter_point: int = None
        self.max_level: int = -1
        self.similarity = CosineSimilarity()
        self.index_io = IndexIO(index_path)
        self.layer_search = LayerSearch(self.nodes, self.similarity)
        self.node_insertion = NodeInsertion(self.nodes, self.similarity, self.config)
        self.index_io.load(self)

    def add(self, vector: List[float], id: int) -> None:
        vector = np.array(vector, dtype=np.float32)
        node = Node(id, vector)
        self.nodes[id] = node
        
        if self.enter_point is None:
            self._initialize_first_node(node)
        else:
            self._add_subsequent_node(node)
        
        self.index_io.save(self)

    def search(self, query: List[float], k: int) -> List[Tuple[int, float]]:
        query = np.array(query, dtype=np.float32)
        if self.enter_point is None:
            return []

        enter_point = self.nodes[self.enter_point]
        current_nearest = self.layer_search.search_top_layers(query, enter_point, self.max_level)
        candidates = self.layer_search.search_bottom_layer(current_nearest, query, self.config.ef_construction)

        results = []
        for node in candidates[:k]:
            similarity = self.similarity.calculate(query, node.vector)
            results.append((node.id, similarity))

        return sorted(results, key=lambda x: x[1], reverse=True)

    def rebuild(self, vectors: List[List[float]], ids: List[int]) -> None:
        self.nodes.clear()
        self.enter_point = None
        self.max_level = -1
        for vector, id in zip(vectors, ids):
            self.add(vector, id)

    def _initialize_first_node(self, node: Node) -> None:
        self.enter_point = node.id
        self.max_level = self.config.ml
        for layer in range(self.config.ml + 1):
            node.neighbors[layer] = []

    def _add_subsequent_node(self, node: Node) -> None:
        level = random_level(self.config.M, len(self.nodes))
        if level > self.max_level:
            self.max_level = level
            self.enter_point = node.id
        self.node_insertion.insert_node(node, level, self.enter_point, self.max_level)