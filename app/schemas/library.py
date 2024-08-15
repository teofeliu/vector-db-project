#app/schemas/library.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class LibraryBase(BaseModel):
    text: str
    embedding: List[float]

class LibraryCreate(LibraryBase):
    pass

class LibraryResponse(LibraryBase):
    pass

class LibraryUpdate(BaseModel):
    text: Optional[str] = None
    embedding: Optional[List[float]] = None

class Library(LibraryBase):
    id: int
    document_id: int

    model_config = ConfigDict(from_attributes=True)