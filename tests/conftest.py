import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from database import Base, get_db
from main import app

# use test database
TEST_DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture(scope="session")
def test_db():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)  # clean up after all tests


@pytest.fixture(scope="function")
def db_session(test_db):
    SessionLocal = sessionmaker(bind=test_db)
    session = SessionLocal()
    yield session
    session.rollback()  # roll back after each test, keeps tests isolated
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
