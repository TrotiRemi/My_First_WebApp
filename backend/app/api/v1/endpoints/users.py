from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.user import user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.db.session import get_db

router = APIRouter()

# 🔹 Route existante
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return user.create(db=db, obj_in=user_in)


# 🔹 Nouvelle route : lister tous les utilisateurs
@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = user.get_multi(db=db)
    return users


# 🔹 Nouvelle route : récupérer un utilisateur par ID
@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user.get(db=db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
