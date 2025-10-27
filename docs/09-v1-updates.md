# 📋 V1 Updates & Changes

## ✅ Completed Features (Session 1)

### Authentication & Security
- ✅ JWT token-based authentication with 7-day expiration
- ✅ Password hashing with bcrypt
- ✅ Active session tracking in database
- ✅ Logout endpoint that invalidates sessions
- ✅ CORS configured for all origins (development)

### Frontend UI/UX
- ✅ Single-page application (SPA) with 3 main views:
  1. **Login/Signup forms** - Initial authentication
  2. **Courses list** - Shows all user's courses with horizontal scroll
  3. **Course detail** - Shows documents organized by type with preview

### Course Management
- ✅ Create courses with title, description, start_date, end_date
- ✅ List user's courses in horizontal scrollable cards
- ✅ Delete courses (with confirmation modal)
- ✅ Course card styling:
  - Compact layout (200px width)
  - Truncated descriptions (2 lines max)
  - Dates displayed
  - Delete button (red × in bottom-left)

### Document Management
- ✅ Create documents from URL or file upload
- ✅ 9 document types with proper categorization:
  - Cours
  - Note cours
  - Exercice
  - Correction d'exercice
  - TP/Lab
  - Correction TP/Lab
  - Partiel
  - Correction Partiel
  - Info sur le cours
- ✅ Documents organized by type in horizontal scrollable rows
- ✅ Delete documents (with confirmation modal)
- ✅ Delete button removes file from disk + database record

### File Upload & Storage
- ✅ File upload endpoint (`POST /documents/upload/{course_id}`)
- ✅ UUID-based filename generation (prevents collisions & path traversal)
- ✅ Local filesystem storage at `/app/uploads`
- ✅ Absolute URL generation for proper file serving across ports
- ✅ File download/serving endpoint with security checks

### Document Preview System
- ✅ **Images** (.jpg, .png, .gif, .webp) - Inline display with thumbnail
- ✅ **PDFs** (.pdf) - Embedded iframe viewer
- ✅ **Markdown** (.md) - Rendered with marked.js library (full HTML rendering)
- ✅ **Text files** (.txt, .html) - iframe display
- ✅ **Word documents** (.doc, .docx) - Download link
- ✅ **Other files** - Generic download link with icon

### UI Layout Improvements
- ✅ **Main page layout**:
  - Title "Mes Cours" top-left
  - "+" button top-right to add courses
  - Courses in horizontal scrollable columns
  
- ✅ **Course detail page layout**:
  - Course info (title, description, dates) top-left
  - "+" button top-right to add documents
  - Documents organized by type in horizontal rows
  - Each type has its own section with title & separator
  
- ✅ **Document card styling**:
  - Compact (200px × auto)
  - Preview images/content scaled down (120px max-height)
  - Smooth horizontal scrolling with styled scrollbar
  - Responsive to content

### Database & Migrations
- ✅ 5 Alembic migrations created:
  1. `a_init_tables.py` - Initial schema (users, courses, documents, events)
  2. `b_add_username_to_users.py` - Added username to users table
  3. `c_add_active_sessions.py` - Created active_sessions table for session tracking
  4. `d_add_dates_to_courses.py` - Added start_date, end_date to courses
  5. `e_add_file_path_to_documents.py` - Added file_path column, made url nullable

### Backend Endpoints
- ✅ Auth endpoints: `/auth/signup`, `/auth/login`, `/auth/logout`, `/auth/me`, `/auth/status`, `/auth/connected`
- ✅ Course endpoints: `GET /courses/`, `POST /courses/`, `DELETE /courses/{id}`
- ✅ Document endpoints:
  - `GET /documents/` - List all user's documents
  - `GET /documents/{id}` - Get single document
  - `GET /documents/course/{course_id}` - List documents in course
  - `POST /documents/` - Create from URL
  - `POST /documents/upload/{course_id}` - Upload file
  - `GET /documents/download/{filename}` - Download/serve file
  - `DELETE /documents/{id}` - Delete document

### Form Management
- ✅ Separate forms for adding courses and documents (not inline)
- ✅ Form reset on navigation
- ✅ Modal confirmations for delete operations
- ✅ Error alerting for failed operations

### Authorization
- ✅ Users can only view/delete their own courses
- ✅ Users can only view/delete documents from their courses
- ✅ DELETE operations verify ownership before execution

---

## 🔮 Next Phase: Social Network Features (V2 Architecture)

### Overview
Transform the application from a personal document manager into a **social learning platform** where users can share and discover educational content.

### Core Concept
- **Privacy Model**: Documents/Courses have visibility settings (Private/Public)
- **Discovery**: Users can browse public content from other users
- **Import System**: Copy public documents to personal account
- **User Profiles**: Public profiles showing user's shared content
- **Engagement**: Like/bookmark public content, follow users

### Detailed Architecture

#### 1. **Database Schema Changes**

**New Tables:**
```
- user_profiles (public_id, bio, avatar_url, created_at)
- visibility_settings (owner_id, course_id, doc_id, visibility: 'private'|'public')
- user_following (follower_id, following_id, created_at)
- document_imports (importer_id, original_doc_id, imported_doc_id, created_at)
- likes (user_id, doc_id/course_id, created_at)
- bookmarks (user_id, doc_id/course_id, created_at)
```

**Modified Tables:**
```
documents:
  + visibility: 'private' | 'public' (default 'private')
  + original_document_id: FK (track if imported)
  + import_count: int (track popularity)

courses:
  + visibility: 'private' | 'public' (default 'private')
  + is_template: bool (true if user wants to share as template)
```

#### 2. **Backend Endpoints (V2)**

**User Discovery:**
- `GET /users/search?q={query}` - Search users by username/bio
- `GET /users/{user_id}/profile` - Get public profile
- `GET /users/{user_id}/public-courses` - List user's public courses
- `GET /users/{user_id}/public-documents` - List user's public documents

**Document Sharing:**
- `PATCH /documents/{id}/visibility` - Toggle public/private (owner only)
- `PATCH /courses/{id}/visibility` - Toggle public/private (owner only)
- `POST /documents/{id}/import` - Copy public document to own account
- `POST /courses/{id}/import` - Copy public course + documents to own account

**Discovery Feed:**
- `GET /feed/trending` - Trending public documents
- `GET /feed/following` - Documents from followed users
- `GET /feed/recommended` - Recommendations based on interests/follows

**Social Actions:**
- `POST /documents/{id}/like` - Like a public document
- `DELETE /documents/{id}/like` - Unlike
- `POST /documents/{id}/bookmark` - Bookmark for later
- `GET /me/bookmarks` - List bookmarked documents
- `POST /users/{id}/follow` - Follow user
- `GET /me/following` - List followed users

#### 3. **Frontend Architecture (V2)**

**New Pages:**
1. **Discovery/Browse** - Trending & recommended documents
2. **User Profile** - Public profile with bio, follow button, public content
3. **Search Results** - Search users and documents
4. **Following Feed** - Feed of documents from followed users
5. **My Bookmarks** - Saved documents
6. **Settings** - Privacy settings, profile editing

**UI Components:**
- User avatar + name on documents (attribution)
- "Import to my account" button on public documents
- Visibility toggle (Private/Public) on own content
- Like & bookmark buttons on public content
- Follow button on user profiles

#### 4. **Import System Design**

**Flow for Importing Documents:**

```
User A views User B's public document
  ↓
User A clicks "Import to my account"
  ↓
Backend creates NEW document in User A's account:
  - title: "[Copy] Original Title"
  - url/file_path: Reference to original file OR copy file
  - original_document_id: Points to User B's doc
  - visibility: 'private' (User A decides to share later)
  - course_id: User A selects destination course
  ↓
Document appears in User A's course
```

**File Storage Strategy (2 options):**

Option 1: **Symbolic References** (Recommended for v2)
- Store reference to original file
- One file serves multiple users
- Saves disk space
- If original deleted → handle gracefully (keep reference, show "deleted" marker)

Option 2: **File Copies**
- Copy file to new location
- Independent of original
- More storage but safer

**Recommendation:** Start with Option 1, allow users to choose on import.

#### 5. **Implementation Roadmap (V2)**

**Phase 2a - User Profiles & Discovery:**
- Create user_profiles table
- Add profile page (read-only for others)
- Add search endpoint

**Phase 2b - Sharing & Imports:**
- Add visibility column to documents/courses
- Create visibility toggle UI
- Implement import endpoints
- Handle file reference system

**Phase 2c - Social Features:**
- Add following system
- Like/bookmark functionality
- Trending feed

**Phase 2d - Feed & Recommendations:**
- Following feed
- Trending algorithm
- Recommendations

#### 6. **Security Considerations (V2)**

- ✅ Verify user owns document before marking public
- ✅ Validate import permissions (document must be public)
- ✅ Rate limit search (prevent user enumeration)
- ✅ Block viewing private content (403 Forbidden)
- ✅ Track import source for audit trail
- ✅ Prevent circular imports (document importing itself)
- ✅ Handle deleted documents gracefully

#### 7. **Privacy & Data**

- Public profiles show: username, bio, avatar, public courses/docs count
- Private profiles show: only own data (403 if not owner)
- Imported documents don't show owner's personal info
- Like/follow data is private to the actor

#### 8. **Performance Optimization (V2)**

- Cache public document lists by user
- Paginate search results (25-50 per page)
- Index on visibility + created_at for trending
- Database views for aggregated stats
- CDN for shared files (future)

#### 9. **Testing Strategy (V2)**

- Unit tests for visibility logic
- Integration tests for import flow
- Permission tests (can't import private docs)
- Edge cases (deleted original, circular imports)
- Load tests for popular documents

---

## Migration Path from V1 → V2

1. **Backward Compatibility**: Default all existing documents to `visibility='private'`
2. **No Breaking Changes**: All existing endpoints work as-is
3. **Gradual Rollout**: Add new endpoints alongside old ones
4. **User Opt-in**: Social features are optional
5. **Database Migrations**: Create all new tables, no need to modify existing

