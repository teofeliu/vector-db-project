import logging
from sqlalchemy.orm import Session
from app.schemas.document import DocumentCreate, Document
from app.crud.crud_document import document as crud_document
from app.services.chunking import ChunkingService
from app.services.vector_db import VectorDBService
from fastapi import HTTPException
import json
import traceback

class DocumentProcessingService:
    def __init__(self, chunking_service: ChunkingService, vector_db_service: VectorDBService):
        self.chunking_service = chunking_service
        self.vector_db_service = vector_db_service

    def process_document(self, db: Session, document: DocumentCreate) -> Document:
        try:
            print(f"Starting to process document: {document.title}")
            
            # create document
            db_document = crud_document.create(db=db, obj_in=document)
            print(f"Document created in database with id: {db_document.id}")

            # chunk document
            chunk_creates = self.chunking_service.chunk_document(db_document.id, db_document.content)
            print(f"Document chunked into {len(chunk_creates)} chunks")

            # add chunks to database and vector database
            for i, chunk_create in enumerate(chunk_creates):
                chunk_data = chunk_create.model_dump()
                try:
                    self.vector_db_service.add_chunk(db, chunk_data)
                    print(f"Chunk {i+1}/{len(chunk_creates)} added to vector database")
                except Exception as chunk_error:
                    print(f"Error adding chunk {i+1} to vector database: {str(chunk_error)}")
                    raise
            print(f"Document processing completed successfully for document id: {db_document.id}")
            return db_document
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")