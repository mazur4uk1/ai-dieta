import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.database import Base
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def engine():
    # Use SQLite for tests
    engine = create_engine("sqlite:///:memory:", echo=False)
    return engine


@pytest.fixture(scope="session")
def create_tables(engine):
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session(engine, create_tables):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client():
    return TestClient(app)