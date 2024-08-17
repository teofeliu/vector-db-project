# app/services/document_processing.py
from sqlalchemy.orm import Session
from app.crud.crud_document import document as crud_document
from app.crud.crud_chunk import chunk as crud_chunk
from app.services.chunking import ChunkingService
from app.services.vector_db import VectorDBService
from app.schemas.document import DocumentCreate
from app.models.document import Document
from fastapi import HTTPException

class DocumentProcessingService:
    def __init__(self, chunking_service: ChunkingService, vector_db_service: VectorDBService):
        self.chunking_service = chunking_service
        self.vector_db_service = vector_db_service

    def process_document(self, db: Session, document: DocumentCreate) -> Document:
        try:
            # Create the document
            db_document = crud_document.create(db=db, obj_in=document)
            
            # Chunk the document
            chunk_creates = self.chunking_service.chunk_document(db_document.id, db_document.content)
            
            # Add chunks to database and vector database
            for chunk_create in chunk_creates:
                print("chunk pre:", type(chunk_create).__name__)
                db_chunk = crud_chunk.create(db=db, obj_in=chunk_create)
            
            return db_document
        except Exception as e:
            # Log the error here
            print(f"Error processing document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")