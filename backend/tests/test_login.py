import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User 

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    """Session DB de test (SQLite mémoire partagée)."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Client FastAPI avec dépendance DB sur la session de test."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    c = TestClient(app)
    try:
        yield c
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!",
    }

# ========== TEST 1: LOGIN RÉUSSI ==========
def test_login_success(client, test_user_data):
    client.post("/api/v1/auth/signup", json=test_user_data)
    
    response = client.post("/api/v1/auth/login", data={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# ========== TEST 2: LOGIN ÉCHEC MOT DE PASSE ==========

def test_login_failure_wrong_password(client, test_user_data):
    client.post("/api/v1/auth/signup", json=test_user_data)
    
    response = client.post("/api/v1/auth/login", data={
        "username": test_user_data["username"],
        "password": "WrongPassword!"
    })
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

# ========== TEST 3: LOGIN ÉCHEC USERNAME ==========
def test_login_failure_wrong_username(client, test_user_data):
    client.post("/api/v1/auth/signup", json=test_user_data)
    
    response = client.post("/api/v1/auth/login", data={
        "username": "nonexistentuser",
        "password": test_user_data["password"]
    })
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


