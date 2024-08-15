# app/crud/crud_chunk.py
from app.crud.base import CRUDBase
from app.models.chunk import Chunk
from sqlalchemy.orm import Session
from typing import Any, Dict

class CRUDChunk(CRUDBase[Chunk]):
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> Chunk:
        db_obj = Chunk(
            text=obj_in['text'],
            embedding_array=obj_in['embedding'],
            chunk_metadata=obj_in['chunk_metadata'],
            document_id=obj_in['document_id']
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

chunk = CRUDChunk(Chunk)