from sqlalchemy.orm import Session
from app.models.chunk import Chunk
from app.schemas.chunk import ChunkCreate, ChunkUpdate
from typing import List
import json

class CRUDChunk:
    def create(self, db: Session, *, obj_in: ChunkCreate) -> Chunk:
        db_obj = Chunk(
            content=obj_in.content,
            embedding=json.dumps(obj_in.embedding),
            document_id=obj_in.document_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Chunk:
        return db.query(Chunk).filter(Chunk.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Chunk]:
        chunks = db.query(Chunk).offset(skip).limit(limit).all()
        for chunk in chunks:
            chunk.embedding = json.loads(chunk.embedding)
        return chunks

    def get_multi_by_ids(self, db: Session, *, ids: List[int]) -> List[Chunk]:
        chunks = db.query(Chunk).filter(Chunk.id.in_(ids)).all()
        for chunk in chunks:
            chunk.embedding = json.loads(chunk.embedding)
        return chunks

chunk = CRUDChunk()