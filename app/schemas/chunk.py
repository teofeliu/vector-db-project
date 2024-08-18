from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict

class ChunkBase(BaseModel):
    content: str
    document_id: int
    chunk_metadata: Optional[Dict] = None

class ChunkCreate(ChunkBase):
    embedding: str 

class ChunkUpdate(ChunkBase):
    pass

class ChunkInDB(ChunkBase):
    id: int
    embedding: str
    model_config = ConfigDict(from_attributes=True)

class ChunkResponse(ChunkBase):
    id: int
    similarity: float
    model_config = ConfigDict(from_attributes=True)