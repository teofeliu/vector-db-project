from typing import Dict, Any
from app.services.indexing.base import VectorIndex
from app.services.indexing.brute_force_index import BruteForceIndex
from app.services.indexing.ivf_index import IVFIndex
from app.services.indexing.hnsw_index import HNSWIndex

class VectorIndexFactory:
    @staticmethod
    def create(index_type: str, index_path: str, **kwargs) -> VectorIndex:
        if index_type == "brute_force":
            return BruteForceIndex(index_path=index_path)
        elif index_type == "ivf":
            n_clusters = kwargs.get('n_clusters', 5)
            return IVFIndex(index_path=index_path, n_clusters=n_clusters)
        elif index_type == "hnsw":
            M = kwargs.get('M', 16)
            ef_construction = kwargs.get('ef_construction', 200)
            ml = kwargs.get('ml', 16)
            return HNSWIndex(index_path=index_path, M=M, ef_construction=ef_construction, ml=ml)
        else:
            raise ValueError(f"Unknown index type: {index_type}")