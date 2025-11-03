# Backend test notes

This project includes pytest-based tests for authentication and data access.

Key points to run tests locally or in CI/CD:

- The FastAPI app imports the `documents` endpoint at startup. That module now respects the `UPLOAD_DIR` environment variable. If not set, it defaults to a writable `./uploads` folder next to the test run. This prevents permission issues in CI.
- Tests use an in-memory SQLite database with `StaticPool` and override `get_db` to keep all operations on the same connection during a test.
- Signup and login/logout tests intentionally reflect the current API behavior:
  - Duplicate email -> 400 `Email already registered`
  - Duplicate username -> 400 `Username already taken`
  - Empty or short password: currently allowed by API (no validation); tests expect 201 and do not check password field in the response.
  - Logout with an invalid or already-removed token returns 200 with `{"message": "Already logged out or token invalid"}`.

## Running tests

Use the project root as the working directory.

Optional env var:

- `UPLOAD_DIR` to specify where uploaded files are stored during tests.

