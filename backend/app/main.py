from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.v1.api import api_router  # ✨ NOUVEAU

# Import les modèles
from app.models import user, course, document, event

# ⚠️ NE PAS créer les tables ici - Alembic s'en charge
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="API for managing courses, documents, and schedules for students.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✨ NOUVEAU : Inclure les routes d'authentification
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the School Organizer API",
        "docs": "/docs",
        "version": "0.1.0"
    }