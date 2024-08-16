# tests/test_models/test_chunk.py
import pytest
from app.models.chunk import Chunk
from app.models.document import Document
from app.crud.crud_chunk import chunk as crud_chunk
from app.crud.crud_document import document as crud_document

def test_create_chunk(db):
    # First, create a document
    document_data = {"title": "Test Document", "content": "Test content", "library_id": 1}
    db_document = crud_document.create(db, obj_in=document_data)
    
    chunk_data = {
        "content": "Test chunk content",
        "embedding": [0.1, 0.2, 0.3],
        "document_id": db_document.id
    }
    db_chunk = crud_chunk.create(db, obj_in=chunk_data)
    assert db_chunk.content == "Test chunk content"
    assert db_chunk.embedding == [0.1, 0.2, 0.3]
    assert db_chunk.document_id == db_document.id

def test_get_chunk(db):
    # Create document and chunk
    document = crud_document.create(db, obj_in={"title": "Test Document", "content": "Test content", "library_id": 1})
    chunk_data = {"content": "Test chunk content", "embedding": [0.1, 0.2, 0.3], "document_id": document.id}
    created_chunk = crud_chunk.create(db, obj_in=chunk_data)
    
    retrieved_chunk = crud_chunk.get(db, id=created_chunk.id)
    assert retrieved_chunk.id == created_chunk.id
    assert retrieved_chunk.content == created_chunk.content

def test_update_chunk(db):
    # Create document and chunk
    document = crud_document.create(db, obj_in={"title": "Test Document", "content": "Test content", "library_id": 1})
    chunk_data = {"content": "Test chunk content", "embedding": [0.1, 0.2, 0.3], "document_id": document.id}
    db_chunk = crud_chunk.create(db, obj_in=chunk_data)
    
    update_data = {"content": "Updated chunk content"}
    updated_chunk = crud_chunk.update(db, db_obj=db_chunk, obj_in=update_data)
    assert updated_chunk.content == "Updated chunk content"
    assert updated_chunk.document_id == document.id

def test_delete_chunk(db):
    # Create document and chunk
    document = crud_document.create(db, obj_in={"title": "Test Document", "content": "Test content", "library_id": 1})
    chunk_data = {"content": "Test chunk content", "embedding": [0.1, 0.2, 0.3], "document_id": document.id}
    db_chunk = crud_chunk.create(db, obj_in=chunk_data)
    
    crud_chunk.remove(db, id=db_chunk.id)
    deleted_chunk = crud_chunk.get(db, id=db_chunk.id)
    assert deleted_chunk is None

def test_chunk_document_relationship(db):
    # Create document and chunk
    document = crud_document.create(db, obj_in={"title": "Test Document", "content": "Test content", "library_id": 1})
    chunk_data = {"content": "Test chunk content", "embedding": [0.1, 0.2, 0.3], "document_id": document.id}
    db_chunk = crud_chunk.create(db, obj_in=chunk_data)
    
    # Test relationship
    assert db_chunk in document.chunks
    assert db_chunk.document == document