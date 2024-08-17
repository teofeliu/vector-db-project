# tests/test_api/test_document.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from app.models.document import Document
from app.services.document_processing import DocumentProcessingService

client = TestClient(app)

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_document_processing_service():
    with patch('app.api.v1.endpoints.document.DocumentProcessingService') as mock:
        yield mock

def assert_document_response(response_data, expected_data):
    for key, value in expected_data.items():
        assert response_data[key] == value, f"Mismatch in {key}: expected {value}, got {response_data[key]}"

def test_create_document_success(mock_document_processing_service, mock_db):
    mock_document = Document(id=1, title="Test Document", content="Test content", library_id=1)
    mock_document_processing_service.return_value.process_document.return_value = mock_document

    response = client.post(
        "/api/v1/documents/",
        json={"title": "Test Document", "content": "Test content", "library_id": 1}
    )

    assert response.status_code == 200
    assert_document_response(response.json(), {
        "id": 1,
        "title": "Test Document",
        "content": "Test content",
        "library_id": 1
    })

def test_create_document_failure(mock_document_processing_service, mock_db):
    mock_document_processing_service.return_value.process_document.side_effect = Exception("Processing failed")

    response = client.post(
        "/api/v1/documents/",
        json={"title": "Test Document", "content": "Test content", "library_id": 1}
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Processing failed"}

def test_get_document(mock_db):
    mock_document = Document(id=1, title="Test Document", content="Test content", library_id=1)
    with patch('app.crud.crud_document.document.get', return_value=mock_document):
        response = client.get("/api/v1/documents/1")

    assert response.status_code == 200
    assert_document_response(response.json(), {
        "id": 1,
        "title": "Test Document",
        "content": "Test content",
        "library_id": 1
    })

def test_update_document(mock_db):
    mock_document = Document(id=1, title="Updated Document", content="Updated content", library_id=1)
    with patch('app.crud.crud_document.document.get', return_value=mock_document):
        with patch('app.crud.crud_document.document.update', return_value=mock_document):
            response = client.put(
                "/api/v1/documents/1",
                json={"title": "Updated Document", "content": "Updated content"}
            )

    assert response.status_code == 200
    assert_document_response(response.json(), {
        "id": 1,
        "title": "Updated Document",
        "content": "Updated content",
        "library_id": 1
    })

def test_delete_document(mock_db):
    mock_document = Document(id=1, title="Test Document", content="Test content", library_id=1)
    with patch('app.crud.crud_document.document.get', return_value=mock_document):
        with patch('app.crud.crud_document.document.remove', return_value=mock_document):
            response = client.delete("/api/v1/documents/1")

    assert response.status_code == 200
    assert_document_response(response.json(), {
        "id": 1,
        "title": "Test Document",
        "content": "Test content",
        "library_id": 1
    })

def test_create_document_empty_content(mock_document_processing_service, mock_db):
    mock_document = Document(id=1, title="Test Document", content="", library_id=1)
    mock_document_processing_service.return_value.process_document.return_value = mock_document

    response = client.post(
        "/api/v1/documents/",
        json={"title": "Test Document", "content": "", "library_id": 1}
    )

    assert response.status_code == 200
    assert_document_response(response.json(), {
        "id": 1,
        "title": "Test Document",
        "content": "",
        "library_id": 1
    })