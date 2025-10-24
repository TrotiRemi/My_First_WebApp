from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(Text, nullable=True)  # URL externe (optionnel)
    file_path = Column(String(500), nullable=True)  # Chemin du fichier uploadé
    type = Column(String(100), nullable=True)  # lecture, exercise, correction
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    course = relationship("Course", back_populates="documents")