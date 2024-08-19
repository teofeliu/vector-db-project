# tests/test_api/test_library.py
import pytest
from app.crud.crud_library import library as crud_library

def test_create_library(client):
    response = client.post(
        "/api/v1/libraries/",
        json={"name": "Test Library", "library_metadata": {"description": "A test library"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Library"
    assert data["library_metadata"] == {"description": "A test library"}
    assert "id" in data

def test_get_library(client):
    # First, create a library
    create_response = client.post(
        "/api/v1/libraries/",
        json={"name": "Get Test Library", "library_metadata": {"description": "A library to get"}}
    )
    created_library = create_response.json()
    
    # Now, get the library
    response = client.get(f"/api/v1/libraries/{created_library['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Get Test Library"
    assert data["id"] == created_library["id"]

def test_update_library(client):
    # First, create a library
    create_response = client.post(
        "/api/v1/libraries/",
        json={"name": "Update Test Library", "library_metadata": {"description": "A library to update"}}
    )
    created_library = create_response.json()
    
    # Now, update the library
    update_data = {"name": "Updated Library"}
    response = client.put(f"/api/v1/libraries/{created_library['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Library"
    assert data["id"] == created_library["id"]

def test_delete_library(client):
    # First, create a library
    create_response = client.post(
        "/api/v1/libraries/",
        json={"name": "Delete Test Library", "library_metadata": {"description": "A library to delete"}}
    )
    created_library = create_response.json()
    
    # Now, delete the library
    response = client.delete(f"/api/v1/libraries/{created_library['id']}")
    assert response.status_code == 200
    
    # Verify that the library has been deleted
    get_response = client.get(f"/api/v1/libraries/{created_library['id']}")
    assert get_response.status_code == 404

def test_get_all_libraries(client):
    # Create a couple of libraries
    client.post("/api/v1/libraries/", json={"name": "Library 1", "library_metadata": {"description": "First library"}})
    client.post("/api/v1/libraries/", json={"name": "Library 2", "library_metadata": {"description": "Second library"}})
    
    # Get all libraries
    response = client.get("/api/v1/libraries/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(library["name"] == "Library 1" for library in data)
    assert any(library["name"] == "Library 2" for library in data)