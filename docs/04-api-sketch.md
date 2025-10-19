# API Endpoints — v1 Sketch

This document describes the planned REST API endpoints for the School Organizer WebApp. Each section includes a table summarizing the methods, paths and descriptions of the routes. Authentication is based on JWT tokens that must be provided in the `Authorization: Bearer <token>` header for protected resources.

## 🔐 Authentication

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/auth/signup` | Register a new user account |
| `POST` | `/api/v1/auth/login` | Authenticate and receive a JWT token |
| `GET` | `/api/v1/users/me` | Retrieve current user profile |

## 📚 Courses

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/courses/` | List all courses belonging to the user |
| `POST` | `/api/v1/courses/` | Create a new course |
| `GET` | `/api/v1/courses/{course_id}` | Retrieve a specific course |
| `PUT` | `/api/v1/courses/{course_id}` | Update a course's title/description |
| `DELETE` | `/api/v1/courses/{course_id}` | Delete a course and its associated data |

## 📄 Documents

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/documents/` | List documents; optionally filter by course |
| `POST` | `/api/v1/documents/` | Create a new document |
| `GET` | `/api/v1/documents/{document_id}` | Retrieve a specific document |
| `PUT` | `/api/v1/documents/{document_id}` | Update a document's metadata |
| `DELETE` | `/api/v1/documents/{document_id}` | Delete a document |

## 🗓️ Events (Schedule)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/events/` | List events; optionally filter by course |
| `POST` | `/api/v1/events/` | Create a new event |
| `GET` | `/api/v1/events/{event_id}` | Retrieve a specific event |
| `PUT` | `/api/v1/events/{event_id}` | Update an event's details |
| `DELETE` | `/api/v1/events/{event_id}` | Delete an event |

## 🔗 Sharing & Importing

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/share/{course_id}` | Generate a share code for a course |
| `POST` | `/api/v1/import` | Import a course using a share code |

## 🤝 Collaboration (v2)

These routes are planned for a future release to allow inviting collaborators to courses.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/courses/{course_id}/invite` | Add a collaborator to a course |
| `DELETE` | `/api/v1/courses/{course_id}/invite/{user_id}` | Remove a collaborator from a course |

## Validation & Errors

The API uses Pydantic schemas to validate request payloads. Errors result in appropriate HTTP status codes (e.g., 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity) with informative messages.