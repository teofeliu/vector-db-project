# app/api/v1/endpoints/library.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.crud.crud_library import library
from app.schemas.library import LibraryCreate, LibraryUpdate, Library as LibrarySchema

router = APIRouter()

@router.post("/", response_model=LibrarySchema)
def create_library(library_in: LibraryCreate, db: Session = Depends(get_db)):
    return library.create(db=db, obj_in=library_in.model_dump())