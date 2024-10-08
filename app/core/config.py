# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Dict, Any

class IndexSettings(BaseSettings):
    type: str
    params: Dict[str, Any] = {}

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    API_V1_STR: str = "/api/v1"
    TESTING: bool = False
    COHERE_API_KEY: Optional[str] = None
    VECTOR_INDEX_PATH: str = "./vector_index"
    VECTOR_INDEX: IndexSettings = IndexSettings(type="hnsw") # hnsw or brute_force

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Chunking parameters
    MIN_CHUNK_SIZE: int = 70
    MAX_CHUNK_SIZE: int = 130
    CHUNK_PADDING: int = 0

    # Embedding model
    EMBEDDING_MODEL: str = "embed-english-v2.0"
    
    # Vector search parameters
    DEFAULT_SEARCH_RESULTS: int = 5
    
    # Index rebuilding
    INDEX_REBUILD_BATCH_SIZE: int = 1000
    
    # HNSW Index parameters
    HNSW_M: int = 16
    HNSW_EF_CONSTRUCTION: int = 200
    HNSW_ML: int = 16

    SIMILARITY_MEASURE: str = "cosine" # cosine, dot_product, euclidean

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()