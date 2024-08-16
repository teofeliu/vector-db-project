# app/services/chunking.py
import re
from typing import List, Tuple

class ChunkingService:
    def __init__(self, min_tokens: int = 300, max_tokens: int = 500, padding: int = 50):
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.padding = padding

    def chunk_document(self, text: str) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            chunk, end = self._create_chunk(text, start)
            chunks.append(chunk)
            start = end  # Start at the end of the current chunk (excluding padding)
        return chunks

    def _create_chunk(self, text: str, start: int) -> Tuple[str, int]:
        # Define the primary window
        window_start = start
        window_end = min(start + self.max_tokens, len(text))

        # Attempt to find the end of a paragraph
        chunk_end = self._find_break(text, window_start, window_end, r'\n\s*\n', reverse=True)
        
        # If no paragraph end found, look for the end of a sentence
        if not chunk_end or chunk_end < start + self.min_tokens:
            chunk_end = self._find_break(text, window_start, window_end, r'[.!?]\s', reverse=True)

        # If no sentence end found, look for a word break (space)
        if not chunk_end or chunk_end < start + self.min_tokens:
            chunk_end = self._find_break(text, window_start, window_end, r'\s', reverse=True)

        # If no suitable break found, use the window end
        if not chunk_end or chunk_end < start + self.min_tokens:
            chunk_end = window_end

        # Apply padding
        chunk_start = max(0, start - self.padding)
        chunk_end = min(len(text), chunk_end + self.padding)

        return text[chunk_start:chunk_end], chunk_end

    def _find_break(self, text: str, start: int, end: int, pattern: str, reverse: bool = False) -> int:
        search_range = text[start:end]
        matches = list(re.finditer(pattern, search_range))
        
        if matches:
            # Return the last match if reverse is True, otherwise return the first match
            match = matches[-1] if reverse else matches[0]
            return start + match.end()
        
        return None

    def _count_tokens(self, text: str) -> int:
        # This is a simple tokenization. In a real-world scenario,
        # you might want to use a more sophisticated tokenizer.
        return len(text.split())

# Usage example
if __name__ == "__main__":
    chunking_service = ChunkingService()
    sample_text = """
    This is a sample document. It contains multiple sentences and paragraphs.

    This is the second paragraph. It also has multiple sentences. We'll use this to test our chunking algorithm.

    Here's a third paragraph. It's a bit shorter.

    And a final one for good measure. Let's see how our algorithm handles this text.
    """
    chunks = chunking_service.chunk_document(sample_text)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:")
        print(chunk)
        print("-" * 50)
