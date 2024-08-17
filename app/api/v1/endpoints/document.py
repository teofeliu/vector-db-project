# app/api/v1/endpoints/document.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.document import DocumentCreate, Document as DocumentSchema
from app.services.document_processing import DocumentProcessingService
from app.services.chunking import ChunkingService
from app.services.vector_db import VectorDBService
import io

router = APIRouter()

@router.post("/upload/", response_model=DocumentSchema)
async def create_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    library_id: int = Form(...),
    db: Session = Depends(get_db),
    chunking_service: ChunkingService = Depends(ChunkingService),
    vector_db_service: VectorDBService = Depends(VectorDBService)
):
    try:
        content = await file.read()
        content = content.decode('utf-8')  # Preserve newlines
        
        document = DocumentCreate(title=title, content=content, library_id=library_id)
        
        document_processing_service = DocumentProcessingService(chunking_service, vector_db_service)
        return document_processing_service.process_document(db, document)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))