# hnsw_index/index_io.py
import json
import os
import numpy as np
from .node import Node

class IndexIO:
    def __init__(self, index_path: str):
        self.index_path = index_path
        self.index_file = os.path.join(index_path, "hnsw_index.json")

    def save(self, index) -> None:
        data = {
            "enter_point": index.enter_point,
            "max_level": index.max_level,
            "nodes": {
                str(id): {
                    "vector": node.vector.tolist(),
                    "neighbors": node.neighbors
                } for id, node in index.nodes.items()
            }
        }
        with open(self.index_file, "w") as f:
            json.dump(data, f)

    def load(self, index) -> None:
        if os.path.exists(self.index_file):
            with open(self.index_file, "r") as f:
                data = json.load(f)
            index.enter_point = data["enter_point"]
            index.max_level = data["max_level"]
            index.nodes = {
                int(id): Node(
                    int(id),
                    np.array(node_data["vector"], dtype=np.float32)
                ) for id, node_data in data["nodes"].items()
            }
            for id, node_data in data["nodes"].items():
                index.nodes[int(id)].neighbors = {int(layer): neighbors for layer, neighbors in node_data["neighbors"].items()}