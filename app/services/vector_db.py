# app/services/vector_db.py
from typing import List, Tuple, Dict
from sqlalchemy.orm import Session
from app.crud.crud_chunk import chunk as crud_chunk
from app.schemas.chunk import ChunkCreate, ChunkResponse
from app.models.chunk import Chunk
from .indexing.factory import VectorIndexFactory
from app.core.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.similarity import get_similarity_measure
import json

class VectorDBService:
    def __init__(self):
        self.similarity_measure = get_similarity_measure()
        self.index = VectorIndexFactory.create(
            index_type=settings.VECTOR_INDEX.type,
            index_path=settings.VECTOR_INDEX_PATH,
            similarity_measure=self.similarity_measure,
            **settings.VECTOR_INDEX.params
        )
        self.embedding_service = EmbeddingService()

    def add_chunk(self, db: Session, chunk_data: dict):
        embedding = self.embedding_service.generate_embedding(chunk_data['content'])
        chunk_data['embedding'] = json.dumps(embedding)
        db_chunk = crud_chunk.create(db, obj_in=chunk_data)
        
        # Add the embedding to the index immediately
        self.index.add(embedding, db_chunk.id)
        
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

    def search(self, db: Session, query_text: str, k: int = 5) -> List[ChunkResponse]:
        query_vector = self.embedding_service.generate_embedding(query_text)
        results = self.index.search(query_vector, k)
        chunk_ids = [id for id, _ in results]
        similarities = [similarity for _, similarity in results]
        chunks = crud_chunk.get_multi_by_ids(db, ids=chunk_ids)
        chunk_responses = []
        for chunk, similarity in zip(chunks, similarities):
            if isinstance(chunk.embedding, str):
                chunk.embedding = json.loads(chunk.embedding)
            chunk_response = ChunkResponse(
                id=chunk.id,
                content=chunk.content,
                document_id=chunk.document_id,
                chunk_metadata=chunk.chunk_metadata,
                similarity=similarity
            )
            chunk_responses.append(chunk_response)
        return chunk_responses

    def rebuild_index(self, db: Session):
        chunks = crud_chunk.get_multi(db)
        vectors = [json.loads(chunk.embedding) if isinstance(chunk.embedding, str) else chunk.embedding for chunk in chunks]
        ids = [chunk.id for chunk in chunks]
        self.index.rebuild(vectors, ids)

    def rebuild_index_batched(self, db: Session, batch_size: int = 1000):
        offset = 0
        while True:
            chunks = crud_chunk.get_multi(db, skip=offset, limit=batch_size)
            if not chunks:
                break
            vectors = [json.loads(chunk.embedding) if isinstance(chunk.embedding, str) else chunk.embedding for chunk in chunks]
            ids = [chunk.id for chunk in chunks]
            if offset == 0:
                self.index.rebuild(vectors, ids)
            else:
                for vector, id in zip(vectors, ids):
                    self.index.add(vector, id)
            offset += batch_size

    def clear_index(self):
        self.index.rebuild([], [])