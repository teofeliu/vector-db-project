# app/services/indexing/base.py
from abc import ABC, abstractmethod
from typing import List, Tuple
from app.services.similarity import SimilarityMeasure

class VectorIndex(ABC):
    def __init__(self, similarity_measure: SimilarityMeasure):
        self.similarity_measure = similarity_measure

    @abstractmethod
    def add(self, vector: List[float], id: int) -> None:
        pass

    @abstractmethod
    def search(self, query: List[float], k: int) -> List[Tuple[int, float]]:
        pass

    @abstractmethod
    def rebuild(self, vectors: List[List[float]], ids: List[int]) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def load(self) -> None:
        pass