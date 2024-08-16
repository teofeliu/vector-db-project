# app/schemas/chunk.py
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Union
import json

class ChunkBase(BaseModel):
    content: str
    embedding: Union[str, List[float]]
    document_id: int

    @field_validator('embedding')
    def validate_embedding(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError('Invalid JSON string for embedding')
        elif isinstance(v, list):
            return v
        raise ValueError('Embedding must be a JSON string or a list of floats')

class ChunkCreate(ChunkBase):
    pass

class ChunkUpdate(ChunkBase):
    pass

class Chunk(ChunkBase):
    id: int

    model_config = ConfigDict(from_attributes=True)