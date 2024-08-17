import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.base import Base, get_db
from app.main import app
from app.services.vector_db import VectorDBService
from app.models.chunk import Chunk

@pytest.fixture(scope="function")
def db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    return next(override_get_db())

@pytest.fixture(scope="function")
def vector_db_service():
    return VectorDBService()

@pytest.fixture(scope="function")
def client(db, vector_db_service):
    app.dependency_overrides[VectorDBService] = lambda: vector_db_service
    
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def clear_database(db, vector_db_service):
    db.query(Chunk).delete()
    db.commit()
    vector_db_service.clear_index()