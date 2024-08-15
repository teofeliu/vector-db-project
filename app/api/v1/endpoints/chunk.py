# app/api/v1/endpoints/chunk.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.vector_db import VectorDBService
from app.schemas.chunk import ChunkCreate, ChunkResponse

router = APIRouter()

@router.post("/", response_model=ChunkResponse)
def create_chunk(chunk: ChunkCreate, db: Session = Depends(get_db)):
    vector_db_service = VectorDBService()
    return vector_db_service.create_chunk(db, chunk.dict())