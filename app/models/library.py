# app/models/library.py
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    metadata = Column(JSON)

    documents = relationship("Document", back_populates="library")