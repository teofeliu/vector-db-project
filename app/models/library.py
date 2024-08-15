# app/models/library.py
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    library_metadata = Column(JSON)

    documents = relationship("Document", back_populates="library")