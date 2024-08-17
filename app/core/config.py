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

settings = Settings()