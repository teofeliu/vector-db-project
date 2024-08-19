# tests/services/test_document_processing.py
import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from app.services.document_processing import DocumentProcessingService
from app.schemas.document import DocumentCreate
from app.models.document import Document
from app.models.chunk import Chunk
from fastapi import HTTPException

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def mock_chunking_service():
    return Mock()

@pytest.fixture
def mock_vector_db_service():
    return Mock()

@pytest.fixture
def document_processing_service(mock_chunking_service, mock_vector_db_service):
    return DocumentProcessingService(mock_chunking_service, mock_vector_db_service)

def test_process_document_success(document_processing_service, mock_db):
    # Arrange
    document = DocumentCreate(title="Test Document", content="Test content", library_id=1)
    mock_db_document = Document(id=1, title="Test Document", content="Test content", library_id=1)
    mock_chunks = [Chunk(id=1, content="Test chunk", embedding=[0.1, 0.2, 0.3], document_id=1)]

    document_processing_service.chunking_service.chunk_document.return_value = mock_chunks
    
    with patch('app.crud.crud_document.document.create', return_value=mock_db_document):
        # Act
        result = document_processing_service.process_document(mock_db, document)

    # Assert
    assert result == mock_db_document
    document_processing_service.chunking_service.chunk_document.assert_called_once_with(mock_db, mock_db_document.id, mock_db_document.content)
    document_processing_service.vector_db_service.add_chunk.assert_called_once_with(mock_db, mock_chunks[0])

def test_process_document_failure(document_processing_service, mock_db):
    # Arrange
    document = DocumentCreate(title="Test Document", content="Test content", library_id=1)
    document_processing_service.chunking_service.chunk_document.side_effect = Exception("Chunking failed")

    with patch('app.crud.crud_document.document.create', return_value=Document()):
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            document_processing_service.process_document(mock_db, document)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Error processing document"

def test_process_document_no_chunks(document_processing_service, mock_db):
    # Arrange
    document = DocumentCreate(title="Test Document", content="Test content", library_id=1)
    mock_db_document = Document(id=1, title="Test Document", content="Test content", library_id=1)
    document_processing_service.chunking_service.chunk_document.return_value = []

    with patch('app.crud.crud_document.document.create', return_value=mock_db_document):
        # Act
        result = document_processing_service.process_document(mock_db, document)

    # Assert
    assert result == mock_db_document
    document_processing_service.chunking_service.chunk_document.assert_called_once_with(mock_db, mock_db_document.id, mock_db_document.content)
    document_processing_service.vector_db_service.add_chunk.assert_not_called()