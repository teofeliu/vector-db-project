# app/services/vector_db.py
from typing import List, Tuple, Type
from sqlalchemy.orm import Session
from app.crud.crud_chunk import chunk as crud_chunk
from app.models.chunk import Chunk
from app.schemas.chunk import ChunkCreate
from app.services.indexing.brute_force import BruteForceIndex
import json

class VectorDBService:
    def __init__(self, index_class: Type[BruteForceIndex] = BruteForceIndex):
        self.index = index_class()

    def add_chunk(self, db: Session, chunk_data: ChunkCreate) -> Chunk:
        chunk_data_dict = chunk_data.model_dump()
        embedding = chunk_data_dict['embedding']
        if isinstance(embedding, str):
            embedding = json.loads(embedding)
        chunk_data_dict['embedding'] = json.dumps(embedding)
        chunk = crud_chunk.create(db, obj_in=chunk_data_dict)
        self.index.add(embedding, chunk.id)
        return chunk

    def search(self, db: Session, query_vector: List[float], k: int) -> List[Chunk]:
        results = self.index.search(query_vector, k)
        chunk_ids = [id for id, _ in results]
        chunks = crud_chunk.get_multi_by_ids(db, ids=chunk_ids)
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