# app/services/indexing/base.py
from abc import ABC, abstractmethod
from typing import List, Tuple

class VectorIndex(ABC):
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