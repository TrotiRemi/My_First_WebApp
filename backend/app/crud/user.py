from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class CRUDUser:
    def create(self, db: Session, obj_in: UserCreate):
        db_user = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_active=True,
            is_superuser=False,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get(self, db: Session, id: int):
        return db.query(User).filter(User.id == id).first()

    def get_multi(self, db: Session):
        return db.query(User).all()


user = CRUDUser()
