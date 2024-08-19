#app/schemas/library.py
from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional

class LibraryBase(BaseModel):
    name: str
    library_metadata: Optional[Dict[str, str]] = {}

class LibraryCreate(LibraryBase):
    pass

class LibraryResponse(LibraryBase):
    pass

class LibraryUpdate(BaseModel):
    name: Optional[str] = None
    library_metadata: Optional[Dict[str, str]] = {}

# this is used automatically by FastAPI for the response
class Library(LibraryBase):
    id: int
    document_id: Dict[str, str] = {}

    model_config = ConfigDict(from_attributes=True)