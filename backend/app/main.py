from fastapi import FastAPI

app = FastAPI(
    title="School Organizer API",
    version="0.1.0",
    description="API for managing courses, documents, and schedules for students."
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the School Organizer API"}

