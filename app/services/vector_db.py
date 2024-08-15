# app/services/vector_db.py
from sqlalchemy.orm import Session
from app.crud.crud_library import library as crud_library
from app.crud.crud_document import document as crud_document
from app.crud.crud_chunk import chunk as crud_chunk
from app.models.library import Library
from app.models.document import Document
from app.models.chunk import Chunk

class VectorDBService:
    def create_library(self, db: Session, library_data: dict):
        return crud_library.create(db, obj_in=library_data)

    def create_document(self, db: Session, document_data: dict, library_id: int):
        document_data['library_id'] = library_id
        return crud_document.create(db, obj_in=document_data)

    def create_chunk(self, db: Session, chunk_data: dict, document_id: int):
        chunk_data['document_id'] = document_id
        return crud_chunk.create(db, obj_in=chunk_data)

    # Add more methods as needed MOREISLEFT