# app/api/v1/endpoints/chunk.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.chunk import ChunkCreate, Chunk as ChunkSchema
from app.services.vector_db import VectorDBService

router = APIRouter()
vector_db_service = VectorDBService()

@router.post("/", response_model=ChunkSchema)
def create_chunk(chunk: ChunkCreate, db: Session = Depends(get_db)):
    return vector_db_service.add_chunk(db, chunk)

@router.get("/{chunk_id}", response_model=ChunkSchema)
def read_chunk(chunk_id: int, db: Session = Depends(get_db)):
    db_chunk = vector_db_service.get_chunk(db, chunk_id)
    if db_chunk is None:
        raise HTTPException(status_code=404, detail="Chunk not found")
    return db_chunk

@router.get("/", response_model=List[ChunkSchema])
def read_chunks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chunks = vector_db_service.get_chunks(db, skip=skip, limit=limit)
    return chunks

@router.post("/search", response_model=List[ChunkSchema])
def search_chunks(query: List[float], k: int = 5, db: Session = Depends(get_db)):
    return vector_db_service.search(db, query, k)