# app/services/chunking.py
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.crud.crud_chunk import chunk as crud_chunk
from app.schemas.chunk import ChunkCreate
from app.services.embedding_service import EmbeddingService
from app.core.config import settings

class ChunkingService:
    def __init__(self):
        self.text_processor = EmbeddingService()

    def find_paragraph_end(self, tokens: List[int], start: int, end: int) -> int:
        for i in range(min(end, len(tokens) - 1)-1, start-1, -1):
            if tokens[i] == 206:  # 206 is \n for cohere tokenizer
                return i
        return 0

    def find_sentence_end(self, tokens: List[int], start: int, end: int) -> int:
        sentence_end_tokens = [21, 8, 38]  # cohere token IDs for '.', '!', '?'
        for i in range(min(end, len(tokens))-1, start-1, -1):
            if tokens[i] in sentence_end_tokens:
                return i + 1
        return 0

    def find_space(self, tokens: List[int], start: int, end: int) -> int:
        space_token = 228  # 228 is space token
        for i in range(min(end, len(tokens))-1, start-1, -1):
            if tokens[i] == space_token:
                return i
        return 0

    def find_chunk_end(self, tokens: List[int], start: int) -> int:
        end = min(start + settings.MAX_CHUNK_SIZE, len(tokens))
        para_end = self.find_paragraph_end(tokens, start + settings.MIN_CHUNK_SIZE, end)
        if para_end:
            return para_end
        sent_end = self.find_sentence_end(tokens, start + settings.MIN_CHUNK_SIZE, end)
        if sent_end:
            return sent_end
        space = self.find_space(tokens, start + settings.MIN_CHUNK_SIZE, end)
        if space:
            return space
        return end

    def chunk_document(self, document_id: int, text: str) -> List[ChunkCreate]:
        try:
            tokens = self.text_processor.tokenize(text)
            chunks = []
            start = 0
            while start < len(tokens):
                chunk_end = self.find_chunk_end(tokens, start)
                if chunk_end <= start:
                    chunk_end = min(start + settings.MAX_CHUNK_SIZE, len(tokens))

                padded_start = max(0, start - settings.CHUNK_PADDING)
                padded_end = min(len(tokens), chunk_end + settings.CHUNK_PADDING)
                chunk_tokens = tokens[padded_start:padded_end]
                
                chunk_text = self.text_processor.detokenize(chunk_tokens)
                embedding = self.text_processor.generate_embedding(chunk_text)
                
                embedding_json = json.dumps(embedding)
                
                chunk = ChunkCreate(
                    content=chunk_text,
                    embedding=embedding_json,
                    document_id=document_id,
                    chunk_metadata={
                        "start_index": padded_start,
                        "end_index": padded_end,
                        "length": padded_end - padded_start
                    }
                )
                chunks.append(chunk)
                start = chunk_end

            return chunks
        except Exception as e:
            print(f"Error in chunk_document: {str(e)}")
            raise