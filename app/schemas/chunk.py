from pydantic import BaseModel, Field, field_validator
from typing import List
import json

class ChunkBase(BaseModel):
    content: str
    embedding: List[float] = Field(..., description="Embedding as a list of floats")
    document_id: int

class ChunkCreate(ChunkBase):
    pass

class ChunkUpdate(ChunkBase):
    pass

class Chunk(ChunkBase):
    id: int

    class Config:
        from_attributes = True

    @field_validator('embedding', mode='before')
    def validate_embedding(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError('Invalid JSON string for embedding')
        elif isinstance(v, list):
            return v
        raise ValueError('Embedding must be a JSON string or a list of floats')