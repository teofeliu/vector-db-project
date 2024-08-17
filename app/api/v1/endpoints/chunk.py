# app/api/v1/endpoints/chunk.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.chunk import ChunkCreate, Chunk as ChunkSchema
from app.schemas.search import SearchQuery
from app.services.vector_db import VectorDBService
from typing import Optional

router = APIRouter()

@router.post("/", response_model=ChunkSchema)
def create_chunk(chunk: ChunkCreate, db: Session = Depends(get_db), vector_db_service: VectorDBService = Depends(VectorDBService)):
    return vector_db_service.add_chunk(db, chunk.model_dump())

@router.get("/{chunk_id}", response_model=ChunkSchema)
def read_chunk(chunk_id: int, db: Session = Depends(get_db), vector_db_service: VectorDBService = Depends(VectorDBService)):
    db_chunk = vector_db_service.get_chunk(db, chunk_id)
    if db_chunk is None:
        raise HTTPException(status_code=404, detail="Chunk not found")
    return db_chunk

@router.get("/", response_model=List[ChunkSchema])
def read_chunks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), vector_db_service: VectorDBService = Depends(VectorDBService)):
    return vector_db_service.get_chunks(db, skip=skip, limit=limit)

@router.post("/search", response_model=List[ChunkSchema])
def search_chunks(
    text: str = Form(..., description="The text to search for"),
    k: Optional[int] = Form(default=5, description="The number of results to return"),
    db: Session = Depends(get_db),
    vector_db_service: VectorDBService = Depends(VectorDBService)
):
    # Ensure k is at least 1 if provided
    k = max(1, k) if k is not None else 5
    results = vector_db_service.search(db, text, k)
    return results