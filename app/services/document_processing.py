# app/services/document_processing.py
from sqlalchemy.orm import Session
from app.schemas.document import DocumentCreate, Document
from app.crud.crud_document import document as crud_document
from app.services.chunking import ChunkingService
from app.services.vector_db import VectorDBService
from fastapi import HTTPException
import json

class DocumentProcessingService:
    def __init__(self, chunking_service: ChunkingService, vector_db_service: VectorDBService):
        self.chunking_service = chunking_service
        self.vector_db_service = vector_db_service

    def process_document(self, db: Session, document: DocumentCreate) -> Document:
        try:
            # create document
            db_document = crud_document.create(db=db, obj_in=document)

            # chunk document
            chunk_creates = self.chunking_service.chunk_document(db_document.id, db_document.content)

            # add chunks to database and vector database
            for chunk_create in chunk_creates:
                chunk_data = chunk_create.model_dump()
                # embedding already a json string so no need to dump
                self.vector_db_service.add_chunk(db, chunk_data)

            return db_document
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")