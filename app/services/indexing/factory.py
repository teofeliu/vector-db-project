# app/services/indexing/factory.py
from typing import Dict, Any
from app.services.indexing.base import VectorIndex
from app.services.indexing.brute_force_index import BruteForceIndex
from app.services.indexing.ivf_index import IVFIndex
from app.services.indexing.hnsw_index.hnsw_index import HNSWIndex
from app.services.indexing.hnsw_index.config import HNSWConfig
from app.core.config import settings

class VectorIndexFactory:
    @staticmethod
    def create(index_type: str, index_path: str, **kwargs) -> VectorIndex:
        if index_type == "brute_force":
            return BruteForceIndex(index_path=index_path)
        elif index_type == "ivf":
            n_clusters = kwargs.get('n_clusters', settings.IVF_N_CLUSTERS)
            return IVFIndex(index_path=index_path, n_clusters=n_clusters)
        elif index_type == "hnsw":
            hnsw_config = HNSWConfig.from_settings()
            return HNSWIndex(index_path=index_path, config=hnsw_config)
        else:
            raise ValueError(f"Unknown index type: {index_type}")