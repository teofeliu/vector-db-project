from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ChunkBase(BaseModel):
    text: str
    embedding: List[float]

class ChunkCreate(ChunkBase):
    pass

class ChunkResponse(ChunkBase):
    pass

class ChunkUpdate(BaseModel):
    text: Optional[str] = None
    embedding: Optional[List[float]] = None

class Chunk(ChunkBase):
    id: int
    document_id: int

    model_config = ConfigDict(from_attributes=True)