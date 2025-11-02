from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserProfileBase(BaseModel):
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_public: bool = True


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_public: Optional[bool] = None


class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserPublicResponse(BaseModel):
    """Réponse pour un profil public d'utilisateur"""
    id: int
    username: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    followers_count: int = 0
    following_count: int = 0
    
    class Config:
        from_attributes = True
