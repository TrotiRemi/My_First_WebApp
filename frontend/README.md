Front-end minimal

Files:
- index.html : simple page with Signup and Login, stores access_token in localStorage and shows welcome message.

How to run locally:
1. From the `frontend` folder run a static server, for example with Python 3:

```powershell
cd frontend
python -m http.server 3000
```

2. Open http://localhost:3000 in your browser.

Notes:
- The backend must be running at http://localhost:8000 (CORS is configured for that origin).
- Signup uses POST /api/v1/auth/signup with JSON body {username,email,password}.
- Login uses POST /api/v1/auth/login with form data (application/x-www-form-urlencoded).
- After login the page displays "Bonjour <username> !" and stores the token in localStorage.
