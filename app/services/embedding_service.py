# app/services/embedding_service.py
import cohere
from typing import List
from app.core.config import settings
import time
import requests

class EmbeddingService:
    def __init__(self):
        if settings.COHERE_API_KEY is None:
            raise ValueError("COHERE_API_KEY is not set in the environment")
        self.co = cohere.Client(api_key=settings.COHERE_API_KEY)

    def tokenize(self, text: str) -> List[int]:
        return self.co.tokenize(text=text, model="command-r").tokens

    def detokenize(self, tokens: List[int]) -> str:
        return self.co.detokenize(tokens=tokens, model="command-r").text

    def generate_embedding(self, text: str, max_retries: int = 1, retry_delay: float = 1.0) -> List[float]:
        for attempt in range(max_retries + 1):
            try:
                response = self.co.embed(texts=[text], model=settings.EMBEDDING_MODEL)
                return response.embeddings[0]
            # very rarely the cohere call returns an error. this tries again once if that happens
            except Exception as e:
                if attempt < max_retries:
                    print(f"Cohere API error: {str(e)}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Max retries reached. Cohere API error: {str(e)}")
                    raise