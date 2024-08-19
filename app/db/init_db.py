# app/db/init_db.py
from app.db.base import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)