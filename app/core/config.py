# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    API_V1_STR: str = "/api/v1"
    TESTING: bool = False
    COHERE_API_KEY: Optional[str] = None
    VECTOR_INDEX_PATH: str = "./vector_index"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Chunking parameters
    MIN_CHUNK_SIZE: int = 50
    MAX_CHUNK_SIZE: int = 100
    CHUNK_PADDING: int = 0
    
    # Vector search parameters
    DEFAULT_SEARCH_RESULTS: int = 5
    
    # Index rebuilding
    INDEX_REBUILD_BATCH_SIZE: int = 1000
    
    # Embedding model
    EMBEDDING_MODEL: str = "embed-english-v2.0"

settings = Settings()