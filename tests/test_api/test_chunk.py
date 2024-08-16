# tests/test_api/test_chunk.py
import pytest

def test_create_chunk(client):
    response = client.post(
        "/api/v1/chunks/",
        json={"content": "Test chunk content", "embedding": [0.1, 0.2, 0.3], "document_id": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test chunk content"
    assert data["embedding"] == [0.1, 0.2, 0.3]
    assert data["document_id"] == 1
    assert "id" in data

def test_get_chunk(client):
    create_response = client.post(
        "/api/v1/chunks/",
        json={"content": "Test chunk to get", "embedding": [0.4, 0.5, 0.6], "document_id": 1}
    )
    created_chunk = create_response.json()
    
    response = client.get(f"/api/v1/chunks/{created_chunk['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test chunk to get"
    assert data["id"] == created_chunk["id"]
    assert data["embedding"] == [0.4, 0.5, 0.6]

def test_get_all_chunks(client):
    client.post("/api/v1/chunks/", json={"content": "Chunk 1", "embedding": [0.1, 0.2, 0.3], "document_id": 1})
    client.post("/api/v1/chunks/", json={"content": "Chunk 2", "embedding": [0.4, 0.5, 0.6], "document_id": 1})
    
    response = client.get("/api/v1/chunks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert any(chunk["content"] == "Chunk 1" for chunk in data)
    assert any(chunk["content"] == "Chunk 2" for chunk in data)

def test_search_chunks(client):
    client.post("/api/v1/chunks/", json={"content": "Test content 1", "embedding": [1.0, 2.0, 3.0], "document_id": 1})
    client.post("/api/v1/chunks/", json={"content": "Test content 2", "embedding": [4.0, 5.0, 6.0], "document_id": 1})
    client.post("/api/v1/chunks/", json={"content": "Test content 3", "embedding": [7.0, 8.0, 9.0], "document_id": 1})

    response = client.post("/api/v1/chunks/search", json={"query": [1.0, 2.0, 3.0], "k": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["content"] == "Test content 1"

def test_search_chunks_empty_db(client):
    response = client.post("/api/v1/chunks/search", json={"query": [1.0, 2.0, 3.0], "k": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0