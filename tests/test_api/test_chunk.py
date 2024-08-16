# tests/test_api/test_chunk.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# write a create chunk (through api)

def test_search_chunks():
    # First, add some chunks
    client.post("/api/v1/chunks/", json={"content": "Test content 1", "embedding": [1.0, 2.0, 3.0], "document_id": 1})
    client.post("/api/v1/chunks/", json={"content": "Test content 2", "embedding": [4.0, 5.0, 6.0], "document_id": 1})
    client.post("/api/v1/chunks/", json={"content": "Test content 3", "embedding": [7.0, 8.0, 9.0], "document_id": 1})

    # Now, perform a search
    response = client.post("/api/v1/chunks/search", json={"query": [1.0, 2.0, 3.0], "k": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["content"] == "Test content 1"  # The first result should be the exact match

def test_search_chunks_empty_db():
    response = client.post("/api/v1/chunks/search", json={"query": [1.0, 2.0, 3.0], "k": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0