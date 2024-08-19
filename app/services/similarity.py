# app/services/similarity.py
import numpy as np
from abc import ABC, abstractmethod

class SimilarityMeasure(ABC):
    @abstractmethod
    def calculate(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        pass

class CosineSimilarity(SimilarityMeasure):
    def calculate(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)