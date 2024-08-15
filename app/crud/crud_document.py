# app/crud/crud_document.py
from app.crud.base import CRUDBase
from app.models.document import Document

class CRUDDocument(CRUDBase[Document]):
    pass

document = CRUDDocument(Document)