# app/services/indexing/hnsw_index/node_insertion.py
from typing import List, Dict
from .node import Node
from .layer_search import LayerSearch

class NodeInsertion:
    def __init__(self, nodes: Dict[int, Node], similarity, config):
        self.nodes = nodes
        self.similarity = similarity
        self.config = config
        self.layer_search = LayerSearch(nodes, similarity)

    def insert_node(self, node: Node, level: int, enter_point_id: int, max_level: int) -> None:
        enter_point = self.nodes[enter_point_id]
        
        for l in range(min(max_level, level), -1, -1):
            neighbors = self.layer_search.search_bottom_layer(enter_point, node.vector, self.config.ef_construction)
            neighbors = self._select_neighbors(node, neighbors, self.config.M, l)
            
            for neighbor in neighbors:
                node.add_neighbor(l, neighbor.id)
                neighbor.add_neighbor(l, node.id)
            
            if neighbors:
                enter_point = neighbors[0]

    def _select_neighbors(self, node: Node, candidates: List[Node], M: int, layer: int) -> List[Node]:
        return sorted(candidates, key=lambda x: self.similarity.calculate(node.vector, x.vector), reverse=True)[:M]