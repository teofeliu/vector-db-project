# app/services/indexing/factory.py
from typing import Dict, Any
from app.services.indexing.base import VectorIndex
from app.services.indexing.brute_force_index import BruteForceIndex
from app.services.indexing.hnsw_index.hnsw_index import HNSWIndex
from app.services.indexing.hnsw_index.config import HNSWConfig
from app.core.config import settings
from app.services.similarity import get_similarity_measure

class VectorIndexFactory:
    @staticmethod
    def create(index_type: str, index_path: str, **kwargs) -> VectorIndex:
        similarity_measure = get_similarity_measure()
        
        if index_type == "brute_force":
            return BruteForceIndex(index_path=index_path, similarity_measure=similarity_measure)
        elif index_type == "hnsw":
            hnsw_config = HNSWConfig.from_settings()
            return HNSWIndex(index_path=index_path, config=hnsw_config, similarity_measure=similarity_measure)
        else:
            raise ValueError(f"Unknown index type: {index_type}")