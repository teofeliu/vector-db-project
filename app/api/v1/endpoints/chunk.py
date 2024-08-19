# app/api/v1/endpoints/chunk.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.chunk import ChunkCreate, ChunkResponse
from app.core.dependencies import get_vector_db_service
from app.services.vector_db import VectorDBService
from pydantic import BaseModel

router = APIRouter()

class SearchQuery(BaseModel):
    query: str
    k: int = 5

@router.post("/", response_model=ChunkResponse)
def create_chunk(chunk: ChunkCreate, db: Session = Depends(get_db), vector_db_service: VectorDBService = Depends(get_vector_db_service)):
    return vector_db_service.add_chunk(db, chunk.model_dump())

@router.get("/{chunk_id}", response_model=ChunkResponse)
def read_chunk(chunk_id: int, db: Session = Depends(get_db), vector_db_service: VectorDBService = Depends(get_vector_db_service)):
    db_chunk = vector_db_service.get_chunk(db, chunk_id)
    if db_chunk is None:
        raise HTTPException(status_code=404, detail="Chunk not found")
    # Convert the database Chunk to a ChunkResponse
    return ChunkResponse(
        id=db_chunk.id,
        content=db_chunk.content,
        document_id=db_chunk.document_id,
        chunk_metadata=db_chunk.chunk_metadata,
        similarity=1.0  # Set a default similarity value for individual chunk retrieval
    )

@router.get("/", response_model=List[ChunkResponse])
def read_chunks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), vector_db_service: VectorDBService = Depends(get_vector_db_service)):
    db_chunks = vector_db_service.get_chunks(db, skip=skip, limit=limit)
    # Convert database Chunks to ChunkResponses
    return [
        ChunkResponse(
            id=chunk.id,
            content=chunk.content,
            document_id=chunk.document_id,
            chunk_metadata=chunk.chunk_metadata,
            similarity=1.0  # Set a default similarity value for listing chunks
        ) for chunk in db_chunks
    ]

@router.post("/search", response_model=List[ChunkResponse])
def search_chunks(search_query: SearchQuery, db: Session = Depends(get_db), vector_db_service: VectorDBService = Depends(get_vector_db_service)):
    results = vector_db_service.search(db, search_query.query, search_query.k)
    return results

@router.post("/rebuild-index")
def rebuild_index(background_tasks: BackgroundTasks, db: Session = Depends(get_db), vector_db_service: VectorDBService = Depends(get_vector_db_service)):
    background_tasks.add_task(vector_db_service.rebuild_index_batched, db)
    return {"message": "Index rebuild started in the background"}