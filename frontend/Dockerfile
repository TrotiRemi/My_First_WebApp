FROM python:3.10-slim

WORKDIR /app

# Install http.server (already in Python stdlib, but we'll use a simple approach)
COPY . .

EXPOSE 3000

# Serve static files on port 3000
CMD ["python", "-m", "http.server", "3000", "--directory", "/app"]
