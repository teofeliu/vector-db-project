# hnsw_index/config.py
from dataclasses import dataclass
from app.core.config import settings

@dataclass
class HNSWConfig:
    M: int
    ef_construction: int
    ml: int

    @classmethod
    def from_settings(cls):
        return cls(
            M=settings.HNSW_M,
            ef_construction=settings.HNSW_EF_CONSTRUCTION,
            ml=settings.HNSW_ML
        )