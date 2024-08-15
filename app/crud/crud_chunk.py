# app/crud/crud_chunk.py
from app.crud.base import CRUDBase
from app.models.chunk import Chunk

class CRUDChunk(CRUDBase[Chunk]):
    pass

chunk = CRUDChunk(Chunk)