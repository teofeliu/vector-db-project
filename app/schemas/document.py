from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class DocumentBase(BaseModel):
    text: str
    embedding: List[float]

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    text: Optional[str] = None
    embedding: Optional[List[float]] = None

class Document(DocumentBase):
    id: int
    document_id: int

    model_config = ConfigDict(from_attributes=True)