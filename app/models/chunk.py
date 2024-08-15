# app/models/chunk.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.config import settings

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    embedding = Column(JSON)  # Store as JSON for SQLite compatibility
    chunk_metadata = Column(JSON)
    document_id = Column(Integer, ForeignKey("documents.id"))

    document = relationship("Document", back_populates="chunks")

    @property
    def embedding_array(self):
        # Convert JSON to list when retrieving
        return self.embedding if isinstance(self.embedding, list) else []

    @embedding_array.setter
    def embedding_array(self, value):
        # Store list as JSON
        self.embedding = value