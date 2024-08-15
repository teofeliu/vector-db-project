# app/models/document.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    metadata = Column(JSON)
    library_id = Column(Integer, ForeignKey("libraries.id"))

    library = relationship("Library", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document")