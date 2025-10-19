# backend/app/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Classe de base SQLAlchemy pour tous les modèles."""
    pass
