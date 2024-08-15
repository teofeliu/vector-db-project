def test_create_document_with_chunks(client, db):
    # Create a library first
    library_response = client.post("/api/v1/libraries/", json={"name": "Test Library"})
    library_id = library_response.json()["id"]

    # Create a document
    document_data = {
        "library_id": library_id,
        "title": "Test Document",
        "content": "This is the first paragraph. This is the second paragraph."
    }
    response = client.post("/api/v1/documents/", json=document_data)
    assert response.status_code == 200
    document = response.json()

    # Check if chunks were created
    chunks_response = client.get(f"/api/v1/documents/{document['id']}/chunks")
    chunks = chunks_response.json()
    assert len(chunks) > 0  # Assuming your chunking logic created at least one chunk