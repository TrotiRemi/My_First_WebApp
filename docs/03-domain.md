# Domain Model (v1)

This document describes the core entities used in the School Organizer WebApp and their attributes. All fields are defined using standard SQL data types. Future versions may extend these models (e.g., to support many-to-many sharing).

## Entities and Fields

### 👤 Users

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Unique identifier |
| `email` | String | Unique email address |
| `hashed_password` | String | Password hash using bcrypt |
| `created_at` | Timestamp | Account creation date/time |
| `is_active` | Boolean | Whether the account is active |
| `is_superuser` | Boolean | Whether the user has administrative privileges |

### 📚 Courses

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Unique identifier |
| `title` | String | Course name |
| `description` | Text | Optional details |
| `user_id` | Integer (FK) | Owner reference → `users.id` |
| `created_at` | Timestamp | Time of creation |

### 📄 Documents

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Unique identifier |
| `title` | String | Document title |
| `url` | Text | Link to the document (URL or file path) |
| `type` | String | Category (e.g., lecture, exercise, correction) |
| `course_id` | Integer (FK) | Reference to the course → `courses.id` |
| `created_at` | Timestamp | Time of insertion |

### 🗓️ Events

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Unique identifier |
| `title` | String | Event title (e.g., Exam, Homework Deadline) |
| `date` | Date | Date of the event |
| `description` | Text | Optional details |
| `course_id` | Integer (FK) | Associated course → `courses.id` |
| `created_at` | Timestamp | Time of insertion |

### 🔗 ShareCode (v2, optional)

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Unique identifier |
| `code` | String | Unique share code |
| `course_id` | Integer (FK) | Course associated with the share code |
| `expires_at` | Timestamp | When the share code becomes invalid |

## Relationships

| Relationship | Description |
|--------------|-------------|
| **User → Courses** | One user may own multiple courses. |
| **Course → Documents** | One course may have multiple documents. |
| **Course → Events** | One course may have multiple events. |
| **Cascades** | Deleting a user removes their courses and content. |
| **Cascades** | Deleting a course removes its documents and events. |

## Notes

- All `created_at` fields default to the current timestamp (`now()`)
- Foreign keys enforce referential integrity and cascade deletions
- ShareCode will be added in a future version to enable importing courses