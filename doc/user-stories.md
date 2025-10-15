# Product Brief — School Organizer WebApp

## Problem
Students have a lot of documents (lectures, exercises, evaluations, projects...) scattered across drives, emails, and different folders. It’s hard to keep everything structured and know what to study or when deadlines are.

## Target users
Students (high school or university) who want a simple and smart dashboard to manage their school life.

## Value proposition
- Centralize all your courses, notes, and documents in one place.
- Organize documents by course and tag (lecture, exercise, correction...).
- Add deadlines and evaluations in a visual schedule.
- Share your structure with a friend (they can import it in one click).
- Create an account with personalized projects and activities.
- Invite other students to collaborate on a course or project.

## MVP (v1 scope)
- User management (signup/login/logout)
- Course management (CRUD)
- Document management (CRUD within a course, just text/URLs for v1)
- Schedule with deadlines (CRUD)
- Simple sharing feature (generate a share code or export JSON)
- Dockerized backend (API + DB)
- Swagger + authentication (JWT)
- Tests for core routes

## Out of scope (for now)
- File uploads (use text URL links for now)
- Real-time collaboration
- Notifications or calendar sync
- Frontend UI (use FastAPI docs)

## Success criteria
- The app runs via `docker compose up`
- All CRUD endpoints work correctly
- JWT authentication works
- Database seeded with example courses
- All tests pass locally
