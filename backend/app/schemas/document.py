from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentBase(BaseModel):
    title: str
    url: str
    type: Optional[str] = None  # lecture, exercise, correction


class DocumentCreate(DocumentBase):
    course_id: int


class DocumentResponse(DocumentBase):
    id: int
    course_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
