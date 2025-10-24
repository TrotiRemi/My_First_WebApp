from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
