# Product Brief — School Organizer WebApp

## Problem

Students juggle countless files and notes — lectures, exercises, evaluations, corrections, and group projects — across various platforms and devices. This fragmentation makes it hard to know what to review or when assignments are due. Existing tools are either overly complex, generic, or poorly tailored to academic workflows.

## Solution

The School Organizer WebApp offers a unified platform where students can:

- 📚 **Store and categorize** all academic documents (lectures, exercises, corrections, etc.)
- **Group files by course** for intuitive navigation
- 🗓️ **Track deadlines and evaluations** with a personal schedule linked to each course
- **Share course structures** with peers so they can reuse a curated organization
- **Collaborate on group projects** by inviting classmates to join a course or activity

## 🌍 Vision

To provide a student-centric management system that simplifies academic life by consolidating learning materials, deadlines, and collaboration into one elegant interface.

## Value Proposition

| Feature | Benefit |
|---------|---------|
| Centralized storage | No more scattered files or missing notes |
| Course-based grouping | All documents and tasks stay tied to their course |
| Integrated deadlines | Never forget an assignment or evaluation date |
| Easy sharing | Reuse structures without manual copying |
| Personal workspace | Each student gets a private, organized account |
| Collaboration support | Work together seamlessly on shared projects |

## 🎓 Target Audience

The primary users are students at universities and engineering schools. They need a lightweight yet powerful solution to organize their coursework, track deadlines, and collaborate with classmates. Teachers or tutors may also use the sharing feature to distribute course materials.

## Minimum Viable Product (MVP)

The first release will include:

1. **User Authentication**: sign up, log in, secure JWT tokens
2. **Course Management**: CRUD operations on courses (title, description)
3. **Document Management**: attach documents (as URLs or metadata) to a course
4. **Schedule Management**: create deadlines and evaluations linked to courses
5. **Sharing**: generate share codes and import shared courses
6. **Test Suite**: automated tests for key endpoints
7. **Dockerized Stack**: Dockerfile and docker-compose for API and DB services

## Out of Scope (v1)

- Real file uploads (v1 uses URLs or text references)
- Real-time editing or messaging features
- Notifications or calendar integration (Google Calendar, etc.)
- Dedicated frontend (we rely on FastAPI docs UI for demonstration)

## Success Criteria

To consider the MVP successful, the following must be true:

- The system starts via `docker compose up` without errors
- Users can register, authenticate and use CRUD features on courses, documents and events
- JWT authentication and authorization protect all private routes
- The test suite passes via `pytest`
- The API documentation is available via Swagger (`/docs`)
- Database migrations and seed scripts run cleanly

## Future Enhancements

- 📤 **File uploads** to store actual documents (local or cloud storage)
- 🕒 **Real-time collaboration** with comments or chat
- **Notifications** for upcoming deadlines
- **External calendar sync** (Google Calendar or iCal)
- **Custom frontend** (React, Vue or Svelte) with a responsive design