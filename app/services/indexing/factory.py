# app/services/indexing/factory.py
from typing import Dict, Any
from .base import VectorIndex
from .brute_force_index import BruteForceIndex
from .ivf_index import IVFIndex

class VectorIndexFactory:
    @staticmethod
    def create(index_type: str, index_path: str, **kwargs) -> VectorIndex:
        if index_type == "brute_force":
            return BruteForceIndex(index_path=index_path)
        elif index_type == "ivf":
            n_clusters = kwargs.get('n_clusters', 5)
            return IVFIndex(index_path=index_path, n_clusters=n_clusters)
        else:
            raise ValueError(f"Unknown index type: {index_type}")