# tests/test_models/test_library.py
import pytest
from app.models.library import Library
from app.crud.crud_library import library as crud_library

def test_create_library(db):
    library_data = {"name": "Test Library", "library_metadata": {"description": "A test library"}}
    db_library = crud_library.create(db, obj_in=library_data)
    assert db_library.name == "Test Library"
    assert db_library.library_metadata == {"description": "A test library"}

def test_get_library(db):
    library_data = {"name": "Test Library", "library_metadata": {"description": "A test library"}}
    db_library = crud_library.create(db, obj_in=library_data)
    retrieved_library = crud_library.get(db, id=db_library.id)
    assert retrieved_library.id == db_library.id
    assert retrieved_library.name == db_library.name

def test_update_library(db):
    library_data = {"name": "Test Library", "library_metadata": {"description": "A test library"}}
    db_library = crud_library.create(db, obj_in=library_data)
    update_data = {"name": "Updated Library"}
    updated_library = crud_library.update(db, db_obj=db_library, obj_in=update_data)
    assert updated_library.name == "Updated Library"
    assert updated_library.library_metadata == {"description": "A test library"}

def test_delete_library(db):
    library_data = {"name": "Test Library", "library_metadata": {"description": "A test library"}}
    db_library = crud_library.create(db, obj_in=library_data)
    crud_library.remove(db, id=db_library.id)
    deleted_library = crud_library.get(db, id=db_library.id)
    assert deleted_library is None