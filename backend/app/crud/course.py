from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate


def create_course(db: Session, course: CourseCreate, user_id: int) -> Course:
    db_course = Course(
        title=course.title,
        description=course.description,
        start_date=course.start_date,
        end_date=course.end_date,
        user_id=user_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_courses_by_user(db: Session, user_id: int) -> list[Course]:
    """Récupérer tous les cours d'un utilisateur"""
    return db.query(Course).filter(Course.user_id == user_id).all()
