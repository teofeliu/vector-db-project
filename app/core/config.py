# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()