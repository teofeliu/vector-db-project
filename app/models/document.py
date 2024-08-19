# app/models/document.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    document_metadata = Column(JSON)
    library_id = Column(Integer, ForeignKey("libraries.id"))
    
    library = relationship("Library", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document")