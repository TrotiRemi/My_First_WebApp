import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import get_db
# S'assurer que les modèles sont connus de SQLAlchemy
from app.models.user import User  # noqa: F401
from app.models.active_session import ActiveSession  # noqa: F401

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
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

# ========== TEST 1 : LOGOUT RÉUSSI ==========
def test_logout_success(client, test_user_data):
    client.post("/api/v1/auth/signup", json=test_user_data)
    response = client.post("/api/v1/auth/login", data={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    token = response.json().get("access_token")
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"  

# ========== TEST 2 : LOGOUT SANS TOKEN ==========
def test_logout_no_token(client):
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 401

# ========== TEST 3 : LOGOUT AVEC TOKEN INVÁLIDE ==========
def test_logout_invalid_token(client):
    response1 = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": "Bearer invalidtoken123"}
    )
    # Le backend renvoie 200 avec un message explicite quand le token est invalide
    assert response1.status_code == 200
    assert response1.json()["message"] == "Already logged out or token invalid"