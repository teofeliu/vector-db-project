# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.base import Base
from app.main import app
from app.services.vector_db import VectorDBService

@pytest.fixture(scope="function")
def test_db():
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
    
    return override_get_db

@pytest.fixture(scope="function")
def vector_db_service():
    return VectorDBService()

@pytest.fixture(scope="function")
def client(test_db, vector_db_service):
    app.dependency_overrides[VectorDBService] = lambda: vector_db_service
    with TestClient(app) as c:
        yield c