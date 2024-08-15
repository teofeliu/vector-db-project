# app/api/v1/endpoints/chunk.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.crud.crud_chunk import chunk

router = APIRouter()

@router.get("/{chunk_id}")
def read_chunk(chunk_id: int, db: Session = Depends(get_db)):
    return chunk.get(db, id=chunk_id)

# You might want other endpoints like:
# - GET /documents/{document_id}/chunks
# - GET /search (for vector similarity search)