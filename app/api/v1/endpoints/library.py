from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.crud.crud_library import library
from app.schemas.library import LibraryCreate, LibraryUpdate, Library as LibrarySchema

router = APIRouter()

@router.post("/", response_model=LibrarySchema)
def create_library(library_in: LibraryCreate, db: Session = Depends(get_db)):
    return library.create(db=db, obj_in=library_in.model_dump())

@router.get("/{library_id}", response_model=LibrarySchema)
def read_library(library_id: int, db: Session = Depends(get_db)):
    db_library = library.get(db=db, id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library

@router.put("/{library_id}", response_model=LibrarySchema)
def update_library(library_id: int, library_in: LibraryUpdate, db: Session = Depends(get_db)):
    db_library = library.get(db=db, id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return library.update(db=db, db_obj=db_library, obj_in=library_in.model_dump())

@router.delete("/{library_id}", response_model=LibrarySchema)
def delete_library(library_id: int, db: Session = Depends(get_db)):
    db_library = library.get(db=db, id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return library.remove(db=db, id=library_id)

@router.get("/", response_model=List[LibrarySchema])
def read_libraries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return library.get_multi(db=db, skip=skip, limit=limit)