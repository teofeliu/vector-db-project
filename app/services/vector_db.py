# app/services/vector_db.py
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.crud.crud_chunk import chunk as crud_chunk
from app.schemas.chunk import ChunkCreate, Chunk as ChunkSchema
from app.models.chunk import Chunk
from app.services.indexing.disk_based_vector_index import DiskBasedVectorIndex
from app.services.embedding_service import EmbeddingService
import json

class VectorDBService:
    def __init__(self, index_path: str):
        self.index = DiskBasedVectorIndex(index_path)
        self.embedding_service = EmbeddingService()

    def add_chunk(self, db: Session, chunk_data: dict):
        # Generate embedding for the chunk content
        embedding = self.embedding_service.generate_embedding(chunk_data['content'])
        chunk_data['embedding'] = json.dumps(embedding)
        db_chunk = crud_chunk.create(db, obj_in=chunk_data)
        self.index.add(embedding, db_chunk.id)
        print("chunk added to vector db")
        return db_chunk

    def get_chunk(self, db: Session, chunk_id: int):
        chunk = crud_chunk.get(db, id=chunk_id)
        if chunk:
            chunk.embedding = json.loads(chunk.embedding)
        return chunk

    def get_chunks(self, db: Session, skip: int = 0, limit: int = 100):
        chunks = crud_chunk.get_multi(db, skip=skip, limit=limit)
        for chunk in chunks:
            chunk.embedding = json.loads(chunk.embedding)
        return chunks[:limit]

    def search(self, db: Session, query_text: str, k: int = 5):
        # Generate embedding for the query text
        query_vector = self.embedding_service.generate_embedding(query_text)
        results = self.index.search(query_vector, k)
        chunk_ids = [id for id, _ in results]
        chunks = crud_chunk.get_multi_by_ids(db, ids=chunk_ids)
        return chunks

    def rebuild_index(self, db: Session):
        chunks = crud_chunk.get_multi(db)
        vectors = [json.loads(chunk.embedding) for chunk in chunks]
        ids = [chunk.id for chunk in chunks]
        self.index.rebuild(vectors, ids)

    def rebuild_index_batched(self, db: Session, batch_size: int = 1000):
        offset = 0
        while True:
            chunks = crud_chunk.get_multi(db, skip=offset, limit=batch_size)
            if not chunks:
                break
            vectors = [json.loads(chunk.embedding) for chunk in chunks]
            ids = [chunk.id for chunk in chunks]
            if offset == 0:
                self.index.rebuild(vectors, ids)
            else:
                for vector, id in zip(vectors, ids):
                    self.index.add(vector, id)
            offset += batch_size

    def clear_index(self):
        self.index.rebuild([], [])