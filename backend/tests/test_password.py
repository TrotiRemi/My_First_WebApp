import pytest
from app.core.security import get_password_hash, verify_password


def test_hash_password_returns_string():

    password = "test123"
    
    hashed = get_password_hash(password)
    
    assert isinstance(hashed, str)
    assert len(hashed) > 0
    assert hashed != password  


def test_hash_password_different_each_time():
    password = "test123"
    
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    assert hash1 != hash2


def test_verify_password_correct():
    password = "test123"
    hashed = get_password_hash(password)
    
    result = verify_password(password, hashed)
    
    assert result is True


def test_verify_password_incorrect():
    password = "test123"
    wrong_password = "wrongpassword"
    hashed = get_password_hash(password)
    
    result = verify_password(wrong_password, hashed)
    
    assert result is False  