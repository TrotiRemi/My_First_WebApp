# backend/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.security import settings  # on réutilise la config de ton fichier security.py

# Création de l'engine SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance FastAPI : donne une session de DB à chaque requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
