# Domain Model (v1)

## Entities

### User
| Field | Type | Description |
|-------|------|-------------|
| id | int | primary key |
| email | string | unique |
| hashed_password | string | bcrypt hashed |
| created_at | datetime | account creation date |
| is_active | bool | default true |

### Course
| Field | Type | Description |
|-------|------|-------------|
| id | int | primary key |
| title | string | course name |
| description | text | optional |
| user_id | int | owner (foreign key to User) |

### Document
| Field | Type | Description |
|-------|------|-------------|
| id | int | primary key |
| title | string | document name |
| url | string | link to the document (no file upload for v1) |
| type | string | “lecture”, “exercise”, “correction”… |
| course_id | int | foreign key to Course |

### Event (Schedule)
| Field | Type | Description |
|-------|------|-------------|
| id | int | primary key |
| title | string | event title |
| date | date | when the evaluation/deadline happens |
| description | string | optional |
| course_id | int | foreign key to Course |

---

## Relations
- One **User** has many **Courses**
- One **Course** has many **Documents** and many **Events**
- (Optional v2) Shared course → n:m between User and Course
