# app/api/v1/endpoints/docunent.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.vector_db import VectorDBService
from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter()

@router.post("/", response_model=DocumentResponse)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    vector_db_service = VectorDBService()
    return vector_db_service.create_document(db, document.dict())