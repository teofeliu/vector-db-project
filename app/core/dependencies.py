# app/core/dependencies.py
from app.services.vector_db import VectorDBService
from app.services.chunking import ChunkingService
from app.core.config import settings

vector_db_service = VectorDBService(settings.VECTOR_INDEX_PATH)
chunking_service = ChunkingService()

def get_vector_db_service():
    return vector_db_service

def get_chunking_service():
    return chunking_service