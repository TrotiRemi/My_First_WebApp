import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models import User, Course, Document

TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Crée une session de test avec BD vierge."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


def test_database_creation():
    tables = Base.metadata.tables.keys()
    expected_tables = {"users", "courses", "documents", "events", "active_sessions"}
    existing_tables = set(tables)
    
    assert expected_tables.issubset(existing_tables), \
        f"Tables manquantes: {expected_tables - existing_tables}"


def test_insert_user(db_session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="fake_hash"
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
