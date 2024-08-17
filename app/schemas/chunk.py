from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict

class ChunkBase(BaseModel):
    content: str
    document_id: int
    chunk_metadata: Optional[Dict] = None

class ChunkCreate(ChunkBase):
    embedding: str  # Keep this for creation, but it won't be in the response

class ChunkUpdate(ChunkBase):
    pass

class ChunkInDB(ChunkBase):
    id: int
    embedding: str  # This is in the database, but won't be in the API response
    model_config = ConfigDict(from_attributes=True)

class ChunkResponse(ChunkBase):
    id: int
    similarity: float
    model_config = ConfigDict(from_attributes=True)