# User Stories

The user stories describe the tasks that our target users (students and collaborators) will perform with the application. Each story highlights the desired functionality and its acceptance criteria.

## 🔐 Authentication

| Story | Acceptance Criteria |
|-------|---------------------|
| As a student, I want to create an account so that my data is secure and private. | `POST /api/v1/auth/signup` returns 201 with a new user; duplicate emails return 400 with a message. |
| As a student, I want to log in with my credentials so I can access my content. | `POST /api/v1/auth/login` returns 200 with a JWT token; invalid credentials return 401. |

## 📚 Course Management

| Story | Acceptance Criteria |
|-------|---------------------|
| As a student, I want to add a course so that I can group related documents together. | `POST /api/v1/courses/` with a title creates the course (status 201). |
| As a student, I want to view my courses to keep track of what I'm studying. | `GET /api/v1/courses/` returns the list of my courses. |
| As a student, I want to edit or delete a course to update my schedule. | `PUT` or `DELETE /api/v1/courses/{id}` updates or removes the course (404 if not found). |

## 📄 Document Management

| Story | Acceptance Criteria |
|-------|---------------------|
| As a student, I want to attach lecture notes, exercises and corrections to a course. | `POST /api/v1/documents/` with title, URL, type and course ID returns 201. |
| As a student, I want to categorize documents by type (lecture, project, correction) to find them easily. | `type` field accepts specific values; invalid types return 422. |
| As a student, I want to update or remove a document to maintain accurate records. | `PUT` or `DELETE /api/v1/documents/{id}` updates or removes the document (404 if not found). |

## 🗓️ Deadlines and Planning

| Story | Acceptance Criteria |
|-------|---------------------|
| As a student, I want to create tasks and deadlines linked to courses so that I never miss important dates. | `POST /api/v1/events/` with title, date, course ID returns 201; invalid dates return 422. |
| As a student, I want to view my upcoming tasks on a timeline or dashboard to plan my study sessions. | `GET /api/v1/events/` returns events sorted by date. |
| As a student, I want to update or delete events as plans change. | `PUT` or `DELETE /api/v1/events/{id}` updates or removes events (404 if not found). |

## 🤝 Collaboration & Sharing

| Story | Acceptance Criteria |
|-------|---------------------|
| As a student, I want to share a course's structure with a friend so they can import it into their own account. | `POST /api/v1/share/{course_id}` returns a share code; `POST /api/v1/import` with a valid code clones the course. |
| As a collaborator, I want to join a project to work with teammates on shared tasks. (v2) | `POST /api/v1/courses/{id}/invite` adds a collaborator; unauthorized invites return 403. |