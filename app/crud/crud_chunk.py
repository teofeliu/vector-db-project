# app/crud/crud_chunk.py
from app.crud.base import CRUDBase
from app.models.chunk import Chunk
from app.schemas.chunk import ChunkCreate, ChunkUpdate
from typing import List
from sqlalchemy.orm import Session

class CRUDChunk(CRUDBase[Chunk]):
    def get_multi_by_ids(self, db: Session, *, ids: List[int]) -> List[Chunk]:
        return db.query(self.model).filter(self.model.id.in_(ids)).all()


chunk = CRUDChunk(Chunk)