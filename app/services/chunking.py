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
        end = min(start + 500, len(tokens))
        para_end = self.find_paragraph_end(tokens, start + 300, end)
        if para_end:
            return para_end
        sent_end = self.find_sentence_end(tokens, start + 300, end)
        if sent_end:
            return sent_end
        space = self.find_space(tokens, start + 300, end)
        if space:
            return space
        return end  # If no suitable break point found, return the maximum end

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