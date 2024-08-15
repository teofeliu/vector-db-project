#tests/test_api/test_library.py
import pytest
#from fastapi.testclient import TestClient

def test_create_library(client):
    response = client.post(
        "/api/v1/libraries/",
        json={"name": "Test Library", "library_metadata": {"description": "A test library"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Library"
    assert "id" in data