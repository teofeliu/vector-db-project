# tests/test_models/test_document.py
import pytest
from app.models.document import Document
from app.crud.crud_document import document as crud_document
from app.crud.crud_library import library as crud_library

def test_create_document(db):
    # First, create a library
    library_data = {"name": "Test Library", "library_metadata": {"description": "A test library"}}
    db_library = crud_library.create(db, obj_in=library_data)
    document_data = {
        "title": "Test Document",
        "content": "This is the content of the test document",
        "document_metadata": {"author": "Test Author"},
        "library_id": db_library.id
    }
    db_document = crud_document.create(db, obj_in=document_data)
    assert db_document.title == "Test Document"
    assert db_document.content == "This is the content of the test document"
    assert db_document.document_metadata == {"author": "Test Author"}
    assert db_document.library_id == db_library.id

def test_get_document(db):
    # Create library and document
    library = crud_library.create(db, obj_in={"name": "Test Library", "library_metadata": {"description": "A test library"}})
    document_data = {
        "title": "Test Document",
        "content": "This is the content of the test document",
        "document_metadata": {},
        "library_id": library.id
    }
    created_document = crud_document.create(db, obj_in=document_data)
    retrieved_document = crud_document.get(db, id=created_document.id)
    assert retrieved_document.id == created_document.id
    assert retrieved_document.title == created_document.title
    assert retrieved_document.content == created_document.content

def test_update_document(db):
    # Create library and document
    library = crud_library.create(db, obj_in={"name": "Test Library", "library_metadata": {"description": "A test library"}})
    document_data = {
        "title": "Test Document",
        "content": "This is the content of the test document",
        "document_metadata": {},
        "library_id": library.id
    }
    db_document = crud_document.create(db, obj_in=document_data)
    update_data = {"title": "Updated Document", "content": "This is the updated content"}
    updated_document = crud_document.update(db, db_obj=db_document, obj_in=update_data)
    assert updated_document.title == "Updated Document"
    assert updated_document.content == "This is the updated content"
    assert updated_document.library_id == library.id

def test_delete_document(db):
    # Create library and document
    library = crud_library.create(db, obj_in={"name": "Test Library", "library_metadata": {"description": "A test library"}})
    document_data = {
        "title": "Test Document",
        "content": "This is the content of the test document",
        "document_metadata": {},
        "library_id": library.id
    }
    db_document = crud_document.create(db, obj_in=document_data)
    crud_document.remove(db, id=db_document.id)
    deleted_document = crud_document.get(db, id=db_document.id)
    assert deleted_document is None

def test_document_library_relationship(db):
    # Create library and document
    library = crud_library.create(db, obj_in={"name": "Test Library", "library_metadata": {"description": "A test library"}})
    document_data = {
        "title": "Test Document",
        "content": "This is the content of the test document",
        "document_metadata": {},
        "library_id": library.id
    }
    db_document = crud_document.create(db, obj_in=document_data)
    # Test relationship
    assert db_document in library.documents
    assert db_document.library == library