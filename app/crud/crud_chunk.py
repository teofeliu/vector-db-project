# app/crud/crud_chunk.py
from app.crud.base import CRUDBase
from app.models.chunk import Chunk
from app.schemas.chunk import ChunkCreate, ChunkUpdate
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import case


class CRUDChunk(CRUDBase[Chunk]):
    def get_multi_by_ids(self, db: Session, *, ids: List[int]) -> List[Chunk]:
        # Create a CASE statement for ordering
        order_case = case(
            {id: index for index, id in enumerate(ids)},
            value=self.model.id
        )
        
        # Query with specific ordering
        return db.query(self.model)\
                 .filter(self.model.id.in_(ids))\
                 .order_by(order_case)\
                 .all()

chunk = CRUDChunk(Chunk)