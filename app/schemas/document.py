# app/schemas/document.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List

class DocumentBase(BaseModel):
    title: str
    content: str
    document_metadata: Optional[Dict] = None

class DocumentCreate(DocumentBase):
    library_id: int

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    document_metadata: Optional[Dict] = None

class Document(DocumentBase):
    id: int
    library_id: int

    model_config = ConfigDict(from_attributes=True)

class DocumentWithChunks(Document):
    chunks: List["ChunkInDocument"]

class ChunkInDocument(BaseModel):
    id: int
    content: str

    model_config = ConfigDict(from_attributes=True)

DocumentWithChunks.model_rebuild()