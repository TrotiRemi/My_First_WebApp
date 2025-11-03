import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import Base
from app.models.user import User  
from app.db.session import get_db

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Crée un client TestClient avec la BD de test."""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Données d'un utilisateur de test."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!"
    }


# ========== TEST 1: SIGNUP RÉUSSI ==========
def test_signup_success(client, test_user_data):
    response = client.post("/api/v1/auth/signup", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data 


# ========== TEST 2: EMAIL DÉJÀ UTILISÉ ==========
def test_signup_duplicate_email(client, test_user_data):
    client.post("/api/v1/auth/signup", json=test_user_data)
    response = client.post("/api/v1/auth/signup", json={
        "username": "otheruser",
        "email": "test@example.com", 
        "password": "AnotherPassword123!"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


# ========== TEST 3: USERNAME DÉJÀ UTILISÉ ==========
def test_signup_duplicate_username(client, test_user_data):
    client.post("/api/v1/auth/signup", json=test_user_data)
    response = client.post("/api/v1/auth/signup", json={
        "username": "testuser", 
        "email": "other@example.com",
        "password": "AnotherPassword123!"
    })
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


# ========== TEST 4: EMAIL INVALIDE ==========
def test_signup_invalid_email(client):
    response = client.post("/api/v1/auth/signup", json={
        "username": "testuser",
        "email": "not-an-email", 
        "password": "Password123!"
    })
    assert response.status_code == 422


# ========== TEST 5: PASSWORD VIDE ==========
def test_signup_empty_password(client):
    response = client.post("/api/v1/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "" 
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data

# ========== TEST 6: PASSWORD TROP COURT ==========
def test_signup_short_password(client):
    response = client.post("/api/v1/auth/signup", json={
        "username": "JhonnyDepp",  
        "email": "test@example.com",
        "password": "123"  
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "JhonnyDepp"
    assert data["email"] == "test@example.com"
    assert "password" not in data

