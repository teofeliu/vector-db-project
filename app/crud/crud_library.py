# app/crud/crud_library.py
from app.crud.base import CRUDBase
from app.models.library import Library

class CRUDLibrary(CRUDBase[Library]):
    pass

library = CRUDLibrary(Library)