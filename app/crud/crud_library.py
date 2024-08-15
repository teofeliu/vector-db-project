# app/crud/crud_library.py
from sqlalchemy.orm import Session
from app.models.library import Library
from app.crud.base import CRUDBase

class CRUDLibrary(CRUDBase[Library]):
    pass

library = CRUDLibrary(Library)