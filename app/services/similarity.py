from abc import ABC, abstractmethod
import numpy as np
from app.core.config import settings

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

class EuclideanDistance(SimilarityMeasure):
    def calculate(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        return -np.linalg.norm(vec1 - vec2)  # Negative to make it a similarity measure

class DotProduct(SimilarityMeasure):
    def calculate(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        return np.dot(vec1, vec2)

def get_similarity_measure() -> SimilarityMeasure:
    similarity_type = settings.SIMILARITY_MEASURE.lower()
    if similarity_type == "cosine":
        return CosineSimilarity()
    elif similarity_type == "euclidean":
        return EuclideanDistance()
    elif similarity_type == "dot_product":
        return DotProduct()
    else:
        raise ValueError(f"Unknown similarity measure: {similarity_type}")