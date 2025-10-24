from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse
from app.crud.course import create_course, get_courses_by_user

router = APIRouter()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def add_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau cours."""
    return create_course(db=db, course=course, user_id=current_user.id)


@router.get("/", response_model=list[CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les cours de l'utilisateur connecté."""
    return get_courses_by_user(db=db, user_id=current_user.id)
