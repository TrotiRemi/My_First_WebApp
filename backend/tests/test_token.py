import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.core.security import create_access_token
from app.core.config import settings


@pytest.mark.unit
class TestAccessTokenGeneration:
    def test_create_access_token_returns_string(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_is_valid_jwt(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded["sub"] == "testuser"
        assert "exp" in decoded

    def test_create_access_token_with_expiration(self):
        data = {"sub": "testuser"}
        expires_delta = timedelta(hours=1)
        token = create_access_token(data, expires_delta)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert "exp" in decoded