# Development Plan (v1)

## Milestones

### M1 — Authentication
- Setup FastAPI project + models
- Signup/login routes + JWT auth
- Tests

### M2 — Courses
- CRUD endpoints
- Ownership by user
- Tests

### M3 — Documents
- CRUD endpoints linked to courses
- Validation
- Tests

### M4 — Events (Schedule)
- CRUD endpoints linked to courses
- Dates validation
- Tests

### M5 — Infrastructure
- Dockerfile + docker-compose (API + PostgreSQL)
- Alembic migrations
- Database seeding script
- README documentation

## Definition of Done
- ✅ All endpoints return correct HTTP codes
- ✅ JWT authentication working
- ✅ Validation errors handled
- ✅ Unit tests green
- ✅ Swagger docs OK
- ✅ `docker compose up` launches working stack
