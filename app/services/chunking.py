import cohere
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.crud.crud_chunk import chunk as crud_chunk

class ChunkingService:
    def __init__(self, api_key: str):
        self.co = cohere.Client(api_key=api_key)

    def tokenize(self, text: str) -> List[int]:
        return self.co.tokenize(text=text, model="command-r").tokens

    def detokenize(self, tokens: List[int]) -> str:
        return self.co.detokenize(tokens=tokens, model="command-r").text

    def generate_embedding(self, text: str) -> List[float]:
        response = self.co.embed(texts=[text], model="embed-english-v2.0")
        return response.embeddings[0]

    def find_paragraph_end(self, tokens: List[int], start: int, end: int) -> int:
        # Look for double newline tokens which often indicate paragraph breaks
        for i in range(start, min(end, len(tokens) - 1)):
            if tokens[i] == 198 and tokens[i+1] == 198:  # 198 is often the newline token
                return i
        return 0  # Return 0 if no paragraph end found

    def find_sentence_end(self, tokens: List[int], start: int, end: int) -> int:
        # Look for common sentence-ending punctuation tokens
        sentence_end_tokens = [13, 14, 15]  # Example token IDs for '.', '!', '?'
        for i in range(start, min(end, len(tokens))):
            if tokens[i] in sentence_end_tokens:
                return i + 1  # Return the position after the punctuation
        return 0  # Return 0 if no sentence end found

    def find_space(self, tokens: List[int], start: int, end: int) -> int:
        # Look for space token
        space_token = 1  # Example token ID for space
        for i in range(start, min(end, len(tokens))):
            if tokens[i] == space_token:
                return i
        return 0  # Return 0 if no space found

def find_chunk_end(self, tokens: List[int], start: int) -> int:
    max_end = min(start + 500, len(tokens))
    min_end = start + 300

    # Look for paragraph end
    for i in range(max_end, min_end, -1):
        if self.is_paragraph_end(tokens, i):
            return i

    # Look for sentence end
    for i in range(max_end, min_end, -1):
        if self.is_sentence_end(tokens, i):
            return i

    # Look for word boundary
    for i in range(max_end, min_end, -1):
        if self.is_word_boundary(tokens, i):
            return i

    # If no suitable break point found, return the maximum end
    return max_end

def is_paragraph_end(self, tokens: List[int], index: int) -> bool:
    # Implement logic to check if this position is a paragraph end
    # For example, check for double newline tokens
    return index < len(tokens) - 1 and tokens[index] == 198 and tokens[index+1] == 198

def is_sentence_end(self, tokens: List[int], index: int) -> bool:
    # Implement logic to check if this position is a sentence end
    # For example, check for period, question mark, or exclamation mark tokens
    sentence_end_tokens = [13, 14, 15]  # Example token IDs for '.', '!', '?'
    return tokens[index] in sentence_end_tokens

def is_word_boundary(self, tokens: List[int], index: int) -> bool:
    # Implement logic to check if this position is a word boundary
    # For example, check for space token
    return tokens[index] == 1  # Assuming 1 is the token ID for space

    def chunk_document(self, db: Session, document_id: int, text: str) -> List[Dict[str, Any]]:
        tokens = self.tokenize(text)
        chunks = []
        start = 0
        while start < len(tokens):
            chunk_end = self.find_chunk_end(tokens, start)
            if chunk_end <= start:
                # Ensure we're always moving forward to prevent infinite loop
                chunk_end = min(start + 500, len(tokens))
            
            padded_start = max(0, start - 50)
            padded_end = min(len(tokens), chunk_end + 50)
            chunk_tokens = tokens[padded_start:padded_end]
            
            # Detokenize to get the chunk text
            chunk_text = self.detokenize(chunk_tokens)
            
            # Generate embedding
            embedding = self.generate_embedding(chunk_text)
            
            # Create metadata
            metadata = {
                "start_index": padded_start,
                "end_index": padded_end,
                "length": padded_end - padded_start
            }
            
            # Create and save Chunk object
            chunk_data = {
                "content": chunk_text,
                "embedding": embedding,
                "document_id": document_id,
                "metadata": metadata
            }
            db_chunk = crud_chunk.create(db, obj_in=chunk_data)
            chunks.append(db_chunk)
            
            # Move to next chunk
            start = chunk_end

        return chunks