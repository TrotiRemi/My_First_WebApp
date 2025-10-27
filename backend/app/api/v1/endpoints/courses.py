from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.course import Course
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


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un cours (seulement le propriétaire peut le faire)."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this course")
    
    db.delete(course)
    db.commit()
