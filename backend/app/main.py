# backend/app/main.py
from app.db.session import get_db
from fastapi import Depends

@app.get("/test-db")
def test_db(db=Depends(get_db)):
    return {"status": "Database session ready!"}
