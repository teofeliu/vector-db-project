from sqlalchemy.orm import Session
from app.models.chunk import Chunk
from app.schemas.chunk import ChunkCreate, ChunkUpdate
from typing import List, Union, Dict, Any
import json

class CRUDChunk:
    def create(self, db: Session, *, obj_in: Union[ChunkCreate, Dict[str, Any]]) -> Chunk:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump()
        
        db_obj = Chunk(
            content=create_data["content"],
            embedding=json.dumps(create_data["embedding"]),
            document_id=create_data["document_id"]
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Chunk:
        return db.query(Chunk).filter(Chunk.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Chunk]:
        return db.query(Chunk).offset(skip).limit(limit).all()

    def get_multi_by_ids(self, db: Session, *, ids: List[int]) -> List[Chunk]:
        return db.query(Chunk).filter(Chunk.id.in_(ids)).all()

chunk = CRUDChunk()