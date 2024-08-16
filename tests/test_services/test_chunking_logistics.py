import pytest
from unittest.mock import Mock, patch
from app.services.chunking import ChunkingService

@pytest.fixture
def mock_cohere_client():
    with patch('cohere.Client') as mock_client:
        yield mock_client.return_value

@pytest.fixture
def chunking_service(mock_cohere_client):
    return ChunkingService("fake_api_key")

def test_tokenize(chunking_service, mock_cohere_client):
    mock_cohere_client.tokenize.return_value.tokens = [1, 2, 3]
    result = chunking_service.tokenize("test text")
    assert result == [1, 2, 3]
    mock_cohere_client.tokenize.assert_called_once_with(text="test text", model="command-r")

def test_detokenize(chunking_service, mock_cohere_client):
    mock_cohere_client.detokenize.return_value.text = "test text"
    result = chunking_service.detokenize([1, 2, 3])
    assert result == "test text"
    mock_cohere_client.detokenize.assert_called_once_with(tokens=[1, 2, 3], model="command-r")

def test_generate_embedding(chunking_service, mock_cohere_client):
    mock_cohere_client.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]
    result = chunking_service.generate_embedding("test text")
    assert result == [0.1, 0.2, 0.3]
    mock_cohere_client.embed.assert_called_once_with(texts=["test text"], model="embed-english-v2.0")

def test_find_paragraph_end():
    service = ChunkingService("fake_api_key")
    tokens = [1, 2, 198, 198, 3, 4]
    assert service.find_paragraph_end(tokens, 0, 6) == 2
    assert service.find_paragraph_end(tokens, 3, 6) == 0

def test_find_sentence_end():
    service = ChunkingService("fake_api_key")
    tokens = [1, 2, 13, 4, 5]
    assert service.find_sentence_end(tokens, 0, 5) == 3
    assert service.find_sentence_end(tokens, 3, 5) == 0

def test_find_space():
    service = ChunkingService("fake_api_key")
    tokens = [2, 3, 1, 4, 5]
    assert service.find_space(tokens, 0, 5) == 2
    assert service.find_space(tokens, 3, 5) == 0

def test_find_chunk_end():
    service = ChunkingService("fake_api_key")
    tokens = [1] * 1000
    tokens[400] = 198
    tokens[401] = 198
    assert service.find_chunk_end(tokens, 0) == 400

@patch('app.crud.crud_chunk.chunk.create')
def test_chunk_document(mock_create_chunk, chunking_service, mock_cohere_client):
    mock_cohere_client.tokenize.return_value.tokens = list(range(1000))
    mock_cohere_client.detokenize.return_value.text = "chunk text"
    mock_cohere_client.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]
    
    mock_db = Mock()
    mock_create_chunk.return_value = {"id": 1, "content": "chunk text"}

    result = chunking_service.chunk_document(mock_db, 1, "long document text")

    assert len(result) > 0
    for chunk in result:
        assert "id" in chunk
        assert chunk["content"] == "chunk text"

    assert mock_create_chunk.call_count > 0
    _, kwargs = mock_create_chunk.call_args
    assert "content" in kwargs["obj_in"]
    assert "embedding" in kwargs["obj_in"]
    assert "document_id" in kwargs["obj_in"]
    assert "metadata" in kwargs["obj_in"]

def test_chunk_document_prevents_infinite_loop(chunking_service, mock_cohere_client):
    # Simulate a situation where find_chunk_end always returns the start index
    chunking_service.find_chunk_end = lambda tokens, start: start
    
    mock_cohere_client.tokenize.return_value.tokens = list(range(1000))
    mock_cohere_client.detokenize.return_value.text = "chunk text"
    mock_cohere_client.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]
    
    mock_db = Mock()
    with patch('app.crud.crud_chunk.chunk.create') as mock_create_chunk:
        mock_create_chunk.return_value = {"id": 1, "content": "chunk text"}
        result = chunking_service.chunk_document(mock_db, 1, "long document text")
    
    # The document should be split into chunks even if find_chunk_end is not working
    assert len(result) > 0
    # The number of chunks should be less than or equal to the number of tokens divided by 500
    assert len(result) <= 1000 // 500 + 1