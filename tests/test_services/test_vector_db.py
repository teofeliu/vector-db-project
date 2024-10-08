#tests/test_services/test_vector_db.py
import pytest
from app.services.vector_db import VectorDBService
from app.crud.crud_chunk import chunk as crud_chunk
from app.models.chunk import Chunk
from sqlalchemy.orm import Session
from app.schemas.chunk import ChunkCreate

def test_vector_db_service_initialization():
    service = VectorDBService()
    assert service.index is not None

def test_vector_db_service_add_chunk(db: Session):
    service = VectorDBService()
    chunk_data = ChunkCreate(
        content="Test content",
        embedding=[1.0, 2.0, 3.0],
        document_id=1
    )
    chunk = service.add_chunk(db, chunk_data)
    assert isinstance(chunk, Chunk)
    assert chunk.content == "Test content"
    assert chunk.embedding == "[1.0, 2.0, 3.0]"  # Note: embedding is stored as a JSON string
    assert chunk.document_id == 1

def test_vector_db_service_search(db: Session):
    service = VectorDBService()
    # Add some chunks
    chunk_data1 = ChunkCreate(content="Test content 1", embedding=[1.0, 2.0, 3.0], document_id=1)
    chunk_data2 = ChunkCreate(content="Test content 2", embedding=[4.0, 5.0, 6.0], document_id=1)
    chunk_data3 = ChunkCreate(content="Test content 3", embedding=[7.0, 8.0, 9.0], document_id=1)
    service.add_chunk(db, chunk_data1)
    service.add_chunk(db, chunk_data2)
    service.add_chunk(db, chunk_data3)

    # Perform a search
    results = service.search(db, [1.0, 2.0, 3.0], k=2)
    assert len(results) == 2
    assert results[0].content == "Test content 1"  # The first result should be the exact match

def test_vector_db_service_search_empty_db(db: Session):
    service = VectorDBService()
    results = service.search(db, [1.0, 2.0, 3.0], k=2)
    assert len(results) == 0

# You might want to add a fixture to set up and tear down the VectorDBService
@pytest.fixture(scope="function")
def vector_db_service():
    service = VectorDBService()
    yield service
    # Add any necessary teardown here

# Then you can use this fixture in your tests
def test_vector_db_service_with_fixture(db: Session, vector_db_service: VectorDBService):
    chunk_data = ChunkCreate(
        content="Test content",
        embedding=[1.0, 2.0, 3.0],
        document_id=1
    )
    chunk = vector_db_service.add_chunk(db, chunk_data)
    assert isinstance(chunk, Chunk)