# Vector DB API

## Overview

This project implements a REST API for indexing and querying documents within a Vector Database. It allows users to manage libraries, documents, and chunks, as well as perform k-Nearest Neighbor vector searches over indexed content.

## Features

- CRUD operations for Libraries, Documents, and Chunks
- Automatic document chunking with customizable parameters
- Vector indexing using HNSW (Hierarchical Navigable Small World) and Brute Force algorithms
- Configurable similarity measures (Cosine, Euclidean, Dot Product)
- Flexible configuration through settings file
- Containerized with Docker and deployable on Kubernetes

## Tech Stack

- Backend: Python + FastAPI + Pydantic
- Database: SQLite
- Vector Embeddings: Cohere API

## API Endpoints

- `/api/v1/libraries`: CRUD operations for libraries
- `/api/v1/documents`: CRUD operations for documents
- `/api/v1/chunks`: CRUD operations for chunks
- `/api/v1/search`: Vector search endpoint

## Configuration

Key settings can be adjusted in `app/core/config.py`, including:

- Chunking parameters (token range, padding)
- Indexing algorithm selection and parameters
- Similarity measure selection
- Embedding model selection

## Automatic Document Chunking

The system employs an intelligent chunking algorithm to divide documents into meaningful segments:

1. Documents are first tokenized using the Cohere tokenizer.
2. Chunks are created within a specified token range (e.g., 70-130 tokens), configurable in settings.
3. The algorithm starts at the maximum token limit and backtrack to find natural break points:
   - First, it looks for paragraph breaks (\n).
   - If no paragraph break is found, it searches for sentence endings.
   - If no sentence end is found, it finds the nearest space.
4. Optionally, chunk padding can be applied to include additional context before and after each chunk.

This approach ensures that chunks maintain semantic coherence while adhering to size constraints, enhancing the quality of vector representations and search results.

## Indexing Algorithms

### Brute Force

- Time Complexity:
  - Search: O(n \* d)
  - Insert: O(1)
- Space Complexity: O(n \* d)

Where n is the number of vectors and d is the vector dimension.

Analysis: Simple to implement and effective for small datasets. Becomes inefficient for large-scale searches.

### HNSW (Hierarchical Navigable Small World)

- Time Complexity:
  - Search: O(log(n) \* d) average case
  - Insert: O(log(n) \* d) average case
- Space Complexity: O(n _ d _ M)

Where n is the number of vectors, d is the vector dimension, and M is the max number of connections per node.

Analysis: Significantly faster searches for large datasets, scales well, but uses more memory due to graph structure.
