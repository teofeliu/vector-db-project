# app/schemas/chunk.py
from pydantic import BaseModel, ConfigDict
from typing import List
import json

class ChunkBase(BaseModel):
    content: str
    embedding: List[float]
    document_id: int

class ChunkCreate(ChunkBase):
    pass

class ChunkUpdate(ChunkBase):
    pass

class Chunk(ChunkBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        # Convert JSON string to list when reading from database
        if isinstance(obj.embedding, str):
            obj.embedding = json.loads(obj.embedding)
        return super().from_orm(obj)