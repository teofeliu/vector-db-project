# app/api/v1/endpoints/document.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.crud.crud_document import document
from app.schemas.document import DocumentCreate, DocumentUpdate, Document as DocumentSchema

router = APIRouter()

@router.post("/", response_model=DocumentSchema)
def create_document(document_in: DocumentCreate, db: Session = Depends(get_db)):
    return document.create(db=db, obj_in=document_in.model_dump())

@router.get("/{document_id}", response_model=DocumentSchema)
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_document = document.get(db=db, id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@router.put("/{document_id}", response_model=DocumentSchema)
def update_document(document_id: int, document_in: DocumentUpdate, db: Session = Depends(get_db)):
    db_document = document.get(db=db, id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document.update(db=db, db_obj=db_document, obj_in=document_in.model_dump(exclude_unset=True))

@router.delete("/{document_id}", response_model=DocumentSchema)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    db_document = document.get(db=db, id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document.remove(db=db, id=document_id)

@router.get("/", response_model=List[DocumentSchema])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return document.get_multi(db=db, skip=skip, limit=limit)