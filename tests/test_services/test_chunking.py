
import pytest
from app.services.chunking import ChunkingService
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.document import Document
from app.crud.crud_document import document as crud_document

@pytest.fixture(scope="module")
def db():
    db = next(get_db())
    yield db
    db.close()

@pytest.fixture(scope="module")
def chunking_service():
    return ChunkingService()

def create_test_document(db: Session, content: str) -> Document:
    document_data = {
        "title": "Test Document",
        "content": content,
        "library_id": 1  # Assuming you have a test library with id 1
    }
    return crud_document.create(db, obj_in=document_data)

def test_chunk_short_document(db: Session, chunking_service: ChunkingService):
    short_text = "This is a very short document."
    document = create_test_document(db, short_text)
    
    chunks = chunking_service.chunk_document(db, document.id, short_text)
    
    assert len(chunks) == 1
    assert chunks[0].content == short_text
    assert len(chunks[0].embedding) > 0  # Ensure embedding was generated

def test_chunk_medium_document(db: Session, chunking_service: ChunkingService):
    medium_text = " ".join([f"This is sentence {i+1} of the medium document." for i in range(120)])
    document = create_test_document(db, medium_text)
    
    chunks = chunking_service.chunk_document(db, document.id, medium_text)

    assert 2 <= len(chunks) <= 4  # Expecting around 3 chunks, but allowing some flexibility
    assert all(200 <= len(chunk.content.split()) <= 500 for chunk in chunks[:-1]) # word range (not tokens)
    assert all(len(chunk.embedding) > 0 for chunk in chunks)  # Ensure embeddings were generated

def test_chunk_long_document(db: Session, chunking_service: ChunkingService):
    # Generate a long string with the pattern "aaa aab aac ... zzz"
    words = [f"{a}{b}{c}" for a in 'abcdefghijklmnopqrstuvwxyz' 
                           for b in 'abcdefghijklmnopqrstuvwxyz' 
                           for c in 'abcdefghijklmnopqrstuvwxyz']
    long_text = " ".join(words)
    
    # Add some newlines and periods to create paragraphs and sentences
    paragraphs = [long_text[i:i+1000] for i in range(0, len(long_text), 1000)]
    long_text_with_structure = "\n\n".join(
        ". ".join(para[i:i+100] for i in range(0, len(para), 100))
        for para in paragraphs
    )
    
    document = create_test_document(db, long_text_with_structure)
    
    chunks = chunking_service.chunk_document(db, document.id, long_text_with_structure)
    
    assert len(chunks) > 10  # Expecting many chunks for this long document
    assert all(200 <= len(chunk.content.split()) <= 400 for chunk in chunks[:-1]) # word range (not tokens)
    assert all(len(chunk.embedding) > 0 for chunk in chunks)  # Ensure embeddings were generated

def test_chunk_consistency(db: Session, chunking_service: ChunkingService):
    # Test that chunking is consistent when done multiple times
    text = " ".join([f"This is sentence {i+1} of the test document." for i in range(50)])
    document = create_test_document(db, text)
    
    chunks1 = chunking_service.chunk_document(db, document.id, text)
    chunks2 = chunking_service.chunk_document(db, document.id, text)
    
    assert len(chunks1) == len(chunks2)
    for c1, c2 in zip(chunks1, chunks2):
        assert c1.content == c2.content
        assert c1.embedding == c2.embedding