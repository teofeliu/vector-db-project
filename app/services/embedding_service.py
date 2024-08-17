# app/services/embedding_service.py
import cohere
from typing import List
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        if settings.COHERE_API_KEY is None:
            raise ValueError("COHERE_API_KEY is not set in the environment")
        self.co = cohere.Client(api_key=settings.COHERE_API_KEY)

    def tokenize(self, text: str) -> List[int]:
        return self.co.tokenize(text=text, model="command-r").tokens

    def detokenize(self, tokens: List[int]) -> str:
        return self.co.detokenize(tokens=tokens, model="command-r").text

    def generate_embedding(self, text: str) -> List[float]:
        response = self.co.embed(texts=[text], model="embed-english-v2.0")
        return response.embeddings[0]