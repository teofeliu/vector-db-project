# app/services/vector_db.py
import json
from typing import List, Tuple, Type
from sqlalchemy.orm import Session
from app.crud.crud_chunk import chunk as crud_chunk
from app.crud.crud_library import library as crud_library
from app.crud.crud_document import document as crud_document
from app.models.chunk import Chunk
from app.schemas.chunk import ChunkCreate
from app.services.indexing.brute_force import BruteForceIndex

class VectorDBService:
    def __init__(self, index_class: Type[BruteForceIndex] = BruteForceIndex):
        self.index = index_class()

    def add_chunk(self, db: Session, chunk_data: ChunkCreate) -> Chunk:
        # Convert embedding list to JSON string
        chunk_data_dict = chunk_data.dict()
        chunk_data_dict['embedding'] = json.dumps(chunk_data_dict['embedding'])
        chunk = crud_chunk.create(db, obj_in=chunk_data_dict)
        self.index.add(chunk_data.embedding, chunk.id)
        return chunk

    def search(self, db: Session, query_vector: List[float], k: int) -> List[Chunk]:
        results = self.index.search(query_vector, k)
        chunk_ids = [id for id, _ in results]
        chunks = crud_chunk.get_multi_by_ids(db, ids=chunk_ids)
        # Convert JSON string back to list
        for chunk in chunks:
            chunk.embedding = json.loads(chunk.embedding)
        return chunks

    def get_chunk(self, db: Session, chunk_id: int) -> Chunk:
        chunk = crud_chunk.get(db, id=chunk_id)
        if chunk:
            chunk.embedding = json.loads(chunk.embedding)
        return chunk

    def get_chunks(self, db: Session, skip: int = 0, limit: int = 100) -> List[Chunk]:
        chunks = crud_chunk.get_multi(db, skip=skip, limit=limit)
        for chunk in chunks:
            chunk.embedding = json.loads(chunk.embedding)
        return chunks

    def create_library(self, db: Session, library_data: dict):
        return crud_library.create(db, obj_in=library_data)

    def create_document(self, db: Session, document_data: dict, library_id: int):
        document_data['library_id'] = library_id
        return crud_document.create(db, obj_in=document_data)

    def create_chunk(self, db: Session, chunk_data: dict, document_id: int):
        chunk_data['document_id'] = document_id
        return crud_chunk.create(db, obj_in=chunk_data)

    # add more methods if needed