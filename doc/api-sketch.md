# API Endpoints (v1 sketch)

## Auth
| Method | Path | Description |
|---------|------|-------------|
| POST | /api/v1/auth/signup | Create account |
| POST | /api/v1/auth/login | Login, returns JWT |
| GET  | /api/v1/users/me | Get current user info |

## Courses
| Method | Path | Description |
|---------|------|-------------|
| GET | /api/v1/courses/ | List my courses |
| POST | /api/v1/courses/ | Create new course |
| GET | /api/v1/courses/{id} | Get details |
| PUT | /api/v1/courses/{id} | Update |
| DELETE | /api/v1/courses/{id} | Delete |

## Documents
| Method | Path | Description |
|---------|------|-------------|
| GET | /api/v1/documents/ | List documents (by course_id param) |
| POST | /api/v1/documents/ | Create a document |
| PUT | /api/v1/documents/{id} | Update document |
| DELETE | /api/v1/documents/{id} | Delete document |

## Events (Schedule)
| Method | Path | Description |
|---------|------|-------------|
| GET | /api/v1/events/ | List all user events |
| POST | /api/v1/events/ | Create new event |
| PUT | /api/v1/events/{id} | Update event |
| DELETE | /api/v1/events/{id} | Delete event |

## Sharing (optional)
| Method | Path | Description |
|---------|------|-------------|
| POST | /api/v1/share/{course_id} | Generate a share code |
| POST | /api/v1/import | Import a shared course |
