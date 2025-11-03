import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import get_db

from app.models.user import User  
from app.models.course import Course  
from app.models.document import Document  
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

# TEST 1 : AJOUT D'UN DOCUMENT RÉUSSI (UPLOAD FICHIER)
def test_upload_document_success(client, test_user_data, tmp_path, monkeypatch):
	assert client.post("/api/v1/auth/signup", json=test_user_data).status_code == 201
	login = client.post(
		"/api/v1/auth/login",
		data={"username": test_user_data["username"], "password": test_user_data["password"]},
	)
	assert login.status_code == 200
	token = login.json()["access_token"]
	headers = {"Authorization": f"Bearer {token}"}
	# Forcer un UPLOAD_DIR temporaire (env + variable du module importé)
	monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
	from app.api.v1.endpoints import documents as documents_module
	monkeypatch.setattr(documents_module, "UPLOAD_DIR", str(tmp_path), raising=False)
	os.makedirs(documents_module.UPLOAD_DIR, exist_ok=True)
	created_course = client.post(
		"/api/v1/courses/", json={"title": "Math 101", "description": "Intro"}, headers=headers
	)
	assert created_course.status_code == 201
	course_id = created_course.json()["id"]
	# Upload the file (use real PDF from tests)
	pdf_path = Path(__file__).parent / "testdata" / "test.pdf"
	pdf_bytes = pdf_path.read_bytes()
	files = {"file": ("test.pdf", pdf_bytes, "application/pdf")}
	data = {"title": "Chapitre 1", "doc_type": "lecture"}
	resp = client.post(f"/api/v1/documents/upload/{course_id}", headers=headers, files=files, data=data)
	assert resp.status_code == 201
	doc = resp.json()
	assert doc["title"] == data["title"]
	assert doc["type"] == data["doc_type"]
	assert doc["course_id"] == course_id
	assert "id" in doc and "created_at" in doc
	assert "/api/v1/documents/download/" in doc["url"]
	filename = doc["url"].split("/download/")[1]
	assert (tmp_path / filename).exists()
# TEST 2 : AJOUT D'UN DOCUMENT SANS NOM (UPLOAD SANS TITLE)
def test_upload_document_missing_title(client, test_user_data, tmp_path, monkeypatch):
	assert client.post("/api/v1/auth/signup", json=test_user_data).status_code == 201
	login = client.post(
		"/api/v1/auth/login",
		data={"username": test_user_data["username"], "password": test_user_data["password"]},
	)
	assert login.status_code == 200
	token = login.json()["access_token"]
	headers = {"Authorization": f"Bearer {token}"}
	# UPLOAD_DIR temporaire (env + variable du module importé)
	monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
	from app.api.v1.endpoints import documents as documents_module
	monkeypatch.setattr(documents_module, "UPLOAD_DIR", str(tmp_path), raising=False)
	os.makedirs(documents_module.UPLOAD_DIR, exist_ok=True)
	created_course = client.post(
		"/api/v1/courses/", json={"title": "Math 101", "description": "Intro"}, headers=headers
	)
	assert created_course.status_code == 201
	course_id = created_course.json()["id"]
	# Uploader un fichier sans title => 422 (title est requis par l'endpoint)
	pdf_path = Path(__file__).parent / "testdata" / "test.pdf"
	pdf_bytes = pdf_path.read_bytes()
	files = {"file": ("test.pdf", pdf_bytes, "application/pdf")}
	resp = client.post(
		f"/api/v1/documents/upload/{course_id}", headers=headers, files=files, data={}
	)
	assert resp.status_code == 422
# TEST 3 : AJOUT D'UN DOCUMENT SANS FICHIER
def test_upload_document_no_file(client, test_user_data, tmp_path, monkeypatch):
    assert client.post("/api/v1/auth/signup", json=test_user_data).status_code == 201
    login = client.post(
        "/api/v1/auth/login",
        data={"username": test_user_data["username"], "password": test_user_data["password"]},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
    from app.api.v1.endpoints import documents as documents_module
    monkeypatch.setattr(documents_module, "UPLOAD_DIR", str(tmp_path), raising=False)
    os.makedirs(documents_module.UPLOAD_DIR, exist_ok=True)
    created_course = client.post(
        "/api/v1/courses/", json={"title": "Math 101", "description": "Intro"}, headers=headers
    )
    assert created_course.status_code == 201
    course_id = created_course.json()["id"]
    data = {"title": "Chapitre 1", "doc_type": "lecture"}
    resp = client.post(
        f"/api/v1/documents/upload/{course_id}", headers=headers, data=data
    )
    assert resp.status_code == 422
# TEST 4 : RÉCUPÉRATION DE LA LISTE DES DOCUMENTS
def test_get_documents_list(client, test_user_data, tmp_path, monkeypatch):
	# Auth
	assert client.post("/api/v1/auth/signup", json=test_user_data).status_code == 201
	login = client.post(
		"/api/v1/auth/login",
		data={"username": test_user_data["username"], "password": test_user_data["password"]},
	)
	assert login.status_code == 200
	token = login.json()["access_token"]
	headers = {"Authorization": f"Bearer {token}"}

	# UPLOAD_DIR temporaire (env + variable du module importé)
	monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
	from app.api.v1.endpoints import documents as documents_module
	monkeypatch.setattr(documents_module, "UPLOAD_DIR", str(tmp_path), raising=False)
	os.makedirs(documents_module.UPLOAD_DIR, exist_ok=True)

	# Créer un cours
	course = client.post(
		"/api/v1/courses/", json={"title": "Course X", "description": "Desc"}, headers=headers
	)
	assert course.status_code == 201
	course_id = course.json()["id"]

	# Uploader 2 documents
	pdf_path = Path(__file__).parent / "testdata" / "test.pdf"
	pdf_bytes = pdf_path.read_bytes()
	for idx in (1, 2):
		files = {"file": (f"test{idx}.pdf", pdf_bytes, "application/pdf")}
		data = {"title": f"Doc {idx}", "doc_type": "lecture"}
		res = client.post(
			f"/api/v1/documents/upload/{course_id}", headers=headers, files=files, data=data
		)
		assert res.status_code == 201

	# Récupérer tous les documents de l'utilisateur
	resp = client.get("/api/v1/documents/", headers=headers)
	assert resp.status_code == 200
	docs = resp.json()
	assert isinstance(docs, list)
	assert len(docs) == 2
	titles = {d["title"] for d in docs}
	assert titles == {"Doc 1", "Doc 2"}
