from sqlalchemy.orm import Session
from app.crud.crud_chunk import chunk as crud_chunk
from app.schemas.chunk import ChunkCreate, Chunk as ChunkSchema
from app.models.chunk import Chunk
from app.services.indexing.brute_force import BruteForceIndex
import json

class VectorDBService:
    def __init__(self):
        self.index = BruteForceIndex()

    def add_chunk(self, db: Session, chunk_data: dict):
        chunk_in = ChunkCreate(**chunk_data)
        db_chunk = crud_chunk.create(db, obj_in=chunk_in)
        self.index.add(chunk_in.embedding, db_chunk.id)
        return db_chunk

    def get_chunk(self, db: Session, chunk_id: int):
        chunk = crud_chunk.get(db, id=chunk_id)
        if chunk:
            chunk.embedding = json.loads(chunk.embedding)
        return chunk

    def get_chunks(self, db: Session, skip: int = 0, limit: int = 100):
        chunks = crud_chunk.get_multi(db, skip=skip, limit=limit)
        return chunks[:limit]

    def search(self, db: Session, query_vector: list, k: int = 5):
        results = self.index.search(query_vector, k)
        chunk_ids = [id for id, _ in results]
        chunks = crud_chunk.get_multi_by_ids(db, ids=chunk_ids)
        # Ensure embeddings are loaded as lists
        for chunk in chunks:
            chunk.embedding = json.loads(chunk.embedding)
        return chunks

    def rebuild_index(self, db: Session):
        chunks = crud_chunk.get_multi(db)
        self.index = BruteForceIndex()
        for chunk in chunks:
            self.index.add(json.loads(chunk.embedding), chunk.id)