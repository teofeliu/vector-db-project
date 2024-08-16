# app/schemas/chunk.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ChunkBase(BaseModel):
    content: str
    embedding: List[float]

class ChunkCreate(ChunkBase):
    document_id: int

class ChunkUpdate(BaseModel):
    content: Optional[str] = None
    embedding: Optional[List[float]] = None

class Chunk(ChunkBase):
    id: int
    document_id: int

    model_config = ConfigDict(from_attributes=True)