from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import create_access_token, verify_password, get_password_hash
from app.db.session import get_db
from app.models.user import User
from app.models.active_session import ActiveSession
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, TokenData

router = APIRouter()

# OAuth2 scheme pour extraire le token du header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
# Scheme optionnel — ne lève pas d'erreur si le token est absent (utile pour /status)
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)


# ========== FONCTIONS UTILITAIRES ==========

def get_user_by_email(db: Session, email: str):
    """Récupère un user par email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    """Récupère un user par username"""
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    """Vérifie les credentials et retourne le user"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Récupère le user connecté depuis le JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Décode le token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # Récupère le user depuis la DB
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


# ========== ROUTES ==========

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Créer un nouveau compte utilisateur
    
    - **username**: Nom d'utilisateur unique
    - **email**: Email unique
    - **password**: Mot de passe (sera hashé)
    """
    # Vérifier si l'email existe déjà
    if get_user_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Vérifier si le username existe déjà
    if get_user_by_username(db, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Créer le user
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Se connecter et recevoir un JWT token
    
    - **username**: Nom d'utilisateur
    - **password**: Mot de passe
    
    Retourne un access_token à utiliser dans le header Authorization
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Créer le JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},  # "sub" = subject = l'identifiant du user
        expires_delta=access_token_expires
    )
    # Enregistrer la session active
    # Calculer expires_at (optionnel)
    import datetime as _dt
    expires_at = _dt.datetime.utcnow() + access_token_expires

    db_session = ActiveSession(user_id=user.id, token=access_token, expires_at=expires_at)
    db.add(db_session)
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/connected")
def list_connected(db: Session = Depends(get_db)):
    """Retourne la liste des users actuellement enregistrés comme connectés (active_sessions)."""
    sessions = db.query(ActiveSession).all()
    result = []
    for s in sessions:
        # Lazy: utiliser la relation user pour récupérer username/email
        result.append({"user_id": s.user_id, "username": s.user.username if s.user else None, "connected_at": s.created_at.isoformat()})
    return result


@router.get("/connected/{user_id}")
def is_user_connected(user_id: int, db: Session = Depends(get_db)):
    """Retourne True si l'utilisateur a au moins une session active."""
    exists = db.query(ActiveSession).filter(ActiveSession.user_id == user_id).first() is not None
    return {"user_id": user_id, "connected": exists}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Récupérer les infos du user connecté
    
    Nécessite un token JWT dans le header Authorization
    """
    return current_user


@router.get("/status")
def auth_status(token: str | None = Depends(oauth2_scheme_optional)):
    """Retourne l'état de connexion sans lever d'erreur si pas de token.

    - connected: True/False
    - username: présent si connecté
    """
    if not token:
        return {"connected": False}

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            return {"connected": False}
        return {"connected": True, "username": username}
    except JWTError:
        return {"connected": False}