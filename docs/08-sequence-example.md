# Example Sequence — Using the API

This example shows a complete sequence of interactions with the School Organizer WebApp API. It demonstrates how a student logs in, creates a course, attaches a document and schedules a deadline. The responses illustrate the expected JSON structure and status codes.

## 1. 🔐 Login

**Request:**

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=student@example.com&password=securepassword
```

**Response — 200 OK:**

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

The returned `access_token` must be included in the `Authorization` header for subsequent requests.

---

## 2. 🆕 Create a Course

**Request:**

```http
POST /api/v1/courses/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "Physics 101",
  "description": "Introduction to Physics"
}
```

**Response — 201 Created:**

```json
{
  "id": 1,
  "title": "Physics 101",
  "description": "Introduction to Physics",
  "user_id": 42,
  "created_at": "2025-10-18T12:00:00Z"
}
```

---

## 3. 📄 Add a Document

**Request:**

```http
POST /api/v1/documents/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "Lecture 1 Slides",
  "url": "https://drive.example.com/physics101/lecture1.pdf",
  "type": "lecture",
  "course_id": 1
}
```

**Response — 201 Created:**

```json
{
  "id": 7,
  "title": "Lecture 1 Slides",
  "url": "https://drive.example.com/physics101/lecture1.pdf",
  "type": "lecture",
  "course_id": 1,
  "created_at": "2025-10-18T12:05:00Z"
}
```

---

## 4. 🗓️ Schedule a Deadline

**Request:**

```http
POST /api/v1/events/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "Homework 1 Due",
  "date": "2025-10-25",
  "description": "Submit problem set via the portal",
  "course_id": 1
}
```

**Response — 201 Created:**

```json
{
  "id": 3,
  "title": "Homework 1 Due",
  "date": "2025-10-25",
  "description": "Submit problem set via the portal",
  "course_id": 1,
  "created_at": "2025-10-18T12:10:00Z"
}
```

---

## 5. 📋 View All Documents for a Course

**Request:**

```http
GET /api/v1/documents/?course_id=1
Authorization: Bearer <JWT_TOKEN>
```

**Response — 200 OK:**

```json
[
  {
    "id": 7,
    "title": "Lecture 1 Slides",
    "url": "https://drive.example.com/physics101/lecture1.pdf",
    "type": "lecture",
    "course_id": 1,
    "created_at": "2025-10-18T12:05:00Z"
  }
]
```

---

## Notes

- All endpoints (except signup) require the JWT token in the `Authorization` header
- The `id` values in responses are examples and will differ in real usage
- The API returns appropriate errors (400, 401, 404, 422) for invalid input or missing data
- This sequence can be extended by updating or deleting items using the corresponding `PUT` and `DELETE` endpoints