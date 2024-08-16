# tests/test_api/test_document.py
import pytest

def test_create_document(client):
    response = client.post(
        "/api/v1/documents/",
        json={"title": "Test Document", "content": "This is a test document", "library_id": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Document"
    assert data["content"] == "This is a test document"
    assert data["library_id"] == 1
    assert "id" in data

def test_get_document(client):
    # First, create a document
    create_response = client.post(
        "/api/v1/documents/",
        json={"title": "Get Test Document", "content": "This is a document to get", "library_id": 1}
    )
    created_document = create_response.json()
    
    # Now, get the document
    response = client.get(f"/api/v1/documents/{created_document['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get Test Document"
    assert data["id"] == created_document["id"]

def test_update_document(client):
    # First, create a document
    create_response = client.post(
        "/api/v1/documents/",
        json={"title": "Update Test Document", "content": "This is a document to update", "library_id": 1}
    )
    created_document = create_response.json()
    
    # Now, update the document
    update_data = {"title": "Updated Document", "content": "This document has been updated"}
    response = client.put(f"/api/v1/documents/{created_document['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Document"
    assert data["content"] == "This document has been updated"
    assert data["id"] == created_document["id"]

def test_delete_document(client):
    # First, create a document
    create_response = client.post(
        "/api/v1/documents/",
        json={"title": "Delete Test Document", "content": "This is a document to delete", "library_id": 1}
    )
    created_document = create_response.json()
    
    # Now, delete the document
    response = client.delete(f"/api/v1/documents/{created_document['id']}")
    assert response.status_code == 200
    
    # Verify that the document has been deleted
    get_response = client.get(f"/api/v1/documents/{created_document['id']}")
    assert get_response.status_code == 404

def test_get_all_documents(client):
    # Create a couple of documents
    client.post("/api/v1/documents/", json={"title": "Document 1", "content": "First document", "library_id": 1})
    client.post("/api/v1/documents/", json={"title": "Document 2", "content": "Second document", "library_id": 1})
    
    # Get all documents
    response = client.get("/api/v1/documents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(document["title"] == "Document 1" for document in data)
    assert any(document["title"] == "Document 2" for document in data)