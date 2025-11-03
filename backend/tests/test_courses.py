import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import get_db

from app.models.user import User  
from app.models.course import Course  
from app.models.active_session import ActiveSession 


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
		"username": "alice",
		"email": "alice@example.com",
		"password": "StrongPass123!",
	}

def test_add_course_success(client, test_user_data):
	signup_resp = client.post("/api/v1/auth/signup", json=test_user_data)
	assert signup_resp.status_code == 201

	login_resp = client.post(
		"/api/v1/auth/login",
		data={
			"username": test_user_data["username"],
			"password": test_user_data["password"],
		},
	)
	assert login_resp.status_code == 200
	token = login_resp.json()["access_token"]

	headers = {"Authorization": f"Bearer {token}"}
	course_payload = {
		"title": "Math 101",
		"description": "Introduction aux mathématiques",
	}

	resp = client.post("/api/v1/courses/", json=course_payload, headers=headers)
	assert resp.status_code == 201
	data = resp.json()
	assert data["title"] == course_payload["title"]
	assert data["description"] == course_payload["description"]
	assert "id" in data and data["id"] > 0
	assert "user_id" in data and isinstance(data["user_id"], int)
	assert "created_at" in data

# TEST 2 : AJOUT D'UN COURS SANS TITRE
def test_add_course_missing_title(client, test_user_data):
	signup_resp = client.post("/api/v1/auth/signup", json=test_user_data)
	assert signup_resp.status_code == 201

	login_resp = client.post(
		"/api/v1/auth/login",
		data={
			"username": test_user_data["username"],
			"password": test_user_data["password"],
		},
	)
	assert login_resp.status_code == 200
	token = login_resp.json()["access_token"]

	headers = {"Authorization": f"Bearer {token}"}
	course_payload = {
		"description": "Introduction aux mathématiques",
	}
	resp = client.post("/api/v1/courses/", json=course_payload, headers=headers)
	assert resp.status_code == 422
# TEST 3 : AJOUT D'UN COURS AVEC UNE DESCRIPTION TROP LONG
def test_add_course_with_long_description(client, test_user_data):
	signup_resp = client.post("/api/v1/auth/signup", json=test_user_data)
	assert signup_resp.status_code == 201

	login_resp = client.post(
		"/api/v1/auth/login",
		data={
			"username": test_user_data["username"],
			"password": test_user_data["password"],
		},
	)
	assert login_resp.status_code == 200
	token = login_resp.json()["access_token"]

	headers = {"Authorization": f"Bearer {token}"}
	course_payload = {
		"title": "Math 101",
		"description": "Introduction aux mathématiques" * 1000,  
	}
	resp = client.post("/api/v1/courses/", json=course_payload, headers=headers)
	assert resp.status_code == 201
# TEST 4 : RÉCUPÉRATION DE LA LISTE DES COURS
def test_get_courses_list(client, test_user_data):
	# Inscription + connexion
	assert client.post("/api/v1/auth/signup", json=test_user_data).status_code == 201
	login_resp = client.post(
		"/api/v1/auth/login",
		data={
			"username": test_user_data["username"],
			"password": test_user_data["password"],
		},
	)
	assert login_resp.status_code == 200
	token = login_resp.json()["access_token"]
	headers = {"Authorization": f"Bearer {token}"}

	# Créer deux cours
	for title in ("Course A", "Course B"):
		resp = client.post(
			"/api/v1/courses/",
			json={"title": title, "description": f"desc {title}"},
			headers=headers,
		)
		assert resp.status_code == 201

	# Récupérer la liste
	list_resp = client.get("/api/v1/courses/", headers=headers)
	assert list_resp.status_code == 200
	courses = list_resp.json()
	assert isinstance(courses, list)
	assert len(courses) == 2
	titles = {c["title"] for c in courses}
	assert titles == {"Course A", "Course B"}
