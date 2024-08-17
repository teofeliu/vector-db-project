# app/models/chunk.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
import json

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    embedding = Column(String)  # Store as JSON string
    document_id = Column(Integer, ForeignKey("documents.id"))
    chunk_metadata = Column(JSON)  # Add this line
    document = relationship("Document", back_populates="chunks")

    @property
    def embedding_list(self):
        return json.loads(self.embedding)

    @embedding_list.setter
    def embedding_list(self, value):
        self.embedding = json.dumps(value)