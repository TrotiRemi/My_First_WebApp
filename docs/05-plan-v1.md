# 🛠️ Development Plan (v1)

## Milestones
1. **M1 — Authentication**
   - User model, hashing (bcrypt), JWT
   - `/auth/signup`, `/auth/login`, `/users/me`
   - Tests (happy path + invalid creds)
2. **M2 — Courses**
   - CRUD + ownership checks
   - List/filter by current user
   - Tests
3. **M3 — Documents**
   - CRUD linked to `course_id`
   - Basic validation (`url` required)
   - Tests
4. **M4 — Events**
   - CRUD with `date` validation
   - Listing by user / course
   - Tests
5. **M5 — Infra & Data**
   - Dockerfile + docker-compose (api+db)
   - Alembic migrations
   - Seed script
   - README + error handling

## Definition of Done
- Correct HTTP codes & bodies
- Validation errors mapped to 422
- Tests green (pytest)
- Swagger docs accessible
- `docker compose up` works

## Future (v2)
- File uploads, roles, calendar sync, notifications, React UI
