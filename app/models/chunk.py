# app/models/chunk.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from .base import Base

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    embedding = Column(ARRAY(Float))
    metadata = Column(JSON)
    document_id = Column(Integer, ForeignKey("documents.id"))

    document = relationship("Document", back_populates="chunks")