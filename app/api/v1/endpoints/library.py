# app/api/v1/endpoints/library.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.vector_db import VectorDBService
from app.schemas.library import LibraryCreate, LibraryResponse

router = APIRouter()

@router.post("/", response_model=LibraryResponse)
def create_library(library: LibraryCreate, db: Session = Depends(get_db)):
    vector_db_service = VectorDBService()
    return vector_db_service.create_library(db, library.dict())