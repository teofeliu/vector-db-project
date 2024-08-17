#app/schemas/chunk.py
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Dict, List
import json

class ChunkBase(BaseModel):
    content: str
    embedding: str  # Keep as string to store JSON in the database
    document_id: int
    chunk_metadata: Optional[Dict] = None

class ChunkCreate(ChunkBase):
    pass

class ChunkUpdate(ChunkBase):
    pass

class Chunk(ChunkBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator('embedding')
    def validate_embedding(cls, v):
        if isinstance(v, str):
            try:
                json.loads(v)  # Ensure it's a valid JSON string
                return v
            except json.JSONDecodeError:
                raise ValueError('Invalid JSON string for embedding')
        elif isinstance(v, list):
            return json.dumps(v)  # Convert list to JSON string
        raise ValueError('Embedding must be a JSON string or a list of floats')