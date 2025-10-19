# 🏗️ Technical Architecture

The School Organizer WebApp is a fullstack application combining a modern Python backend with a relational database and containerized infrastructure. This document describes the high-level architecture, layer responsibilities, folder structure, security considerations, and infrastructure setup.

## Component Overview

| Layer | Technology | Responsibility |
|-------|------------|----------------|
| **API** | FastAPI (Python) | Handle HTTP requests, routing, validation and response generation |
| **Database** | PostgreSQL 16 | Persist data (users, courses, documents, events) |
| **ORM** | SQLAlchemy 2.x | Map Python models to database tables |
| **Validation** | Pydantic 2.x | Validate input and serialize responses |
| **Auth** | JWT + Passlib | Secure authentication with token issuance and password hashing |
| **Infrastructure** | Docker + Compose | Containerize and orchestrate the API and database |
| **Migrations** | Alembic | Manage schema versioning and upgrades |
| **Testing** | Pytest + Httpx | Provide unit and integration test framework |

## Logical Flow

1. **Client / Browser** → Sends HTTP requests (e.g., login, create course)
2. **FastAPI Backend** → Processes requests, applies business logic, validates data and handles auth
3. **Database (PostgreSQL)** → Stores persistent entities; accessed via SQLAlchemy sessions
4. **Containerization (Docker)** → Encapsulates the API and database in isolated services
5. **Migrations (Alembic)** → Applies schema changes and seeds initial data

### Visual Text Diagram

```
Client (browser) → FastAPI → PostgreSQL
                      ↑
                      │
            Swagger UI for interactive API docs
```

## 🗂️ Folder Structure

```
school-organizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── api.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── auth.py
│   │   │           ├── courses.py
│   │   │           ├── documents.py
│   │   │           └── events.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── init_db.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── course.py
│   │   │   ├── document.py
│   │   │   └── event.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── course.py
│   │   │   ├── document.py
│   │   │   ├── event.py
│   │   │   └── token.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py
│   │       └── test_auth.py
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   ├── PRODUCT_BRIEF.md
│   ├── USER_STORIES.md
│   ├── DOMAIN_MODEL.md
│   ├── API_ENDPOINTS.md
│   ├── DEVELOPMENT_PLAN.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   └── API_EXAMPLE.md
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🔒 Security & Config

- **Authentication**: Users log in via `/auth/login` and receive a JWT token. This token is required in the `Authorization` header for all protected routes.
- **Password Hashing**: User passwords are hashed using bcrypt via Passlib; plain text passwords are never stored.
- **Environment Variables**: Sensitive settings (secret key, database credentials) are loaded from a `.env` file using Pydantic settings.
- **Ownership Checks**: The API ensures that users only interact with their own courses, documents and events.

## Infrastructure (Docker Compose)

```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  api:
    build: ./backend
    env_file: .env
    depends_on:
      - db
    ports:
      - "8000:8000"
    command: >
      sh -c "alembic upgrade head && \
             python -m app.db.init_db && \
             uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

volumes:
  pgdata:
```

In this configuration:

- The `db` service runs PostgreSQL and persists data using a named volume (`pgdata`)
- The `api` service builds the FastAPI app, applies database migrations and seeds data before starting the Uvicorn server with automatic reloading in development mode

## Testing & Continuous Integration

- **Unit Tests**: Located in `backend/tests/`, tests check individual functions and classes
- **Integration Tests**: Use `httpx` to simulate API calls and verify end-to-end behavior (including auth and validation)
- **Continuous Integration (CI)**: A GitHub Actions workflow can automatically run linting (e.g., `black`, `flake8`) and tests on each push to avoid regressions

## Future Directions

Future architecture enhancements may include:

- Adding a React or Vue frontend that consumes the API
- Integrating a reverse proxy (e.g., Nginx) for static assets and TLS termination
- Using an object storage service (e.g., Amazon S3) for file uploads
- Monitoring and logging (e.g., Prometheus, Grafana) for performance and error tracking