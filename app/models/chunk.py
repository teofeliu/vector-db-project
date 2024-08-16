# app/models/chunk.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class Chunk(Base):
    __tablename__ = "chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    embedding = Column(JSON)
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    document = relationship("Document", back_populates="chunks")