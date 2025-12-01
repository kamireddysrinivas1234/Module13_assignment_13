import os
import time

from app.security import hash_password, verify_password, create_access_token

def test_hash_and_verify_password_roundtrip():
    pwd = "StrongPass123!"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrong", hashed) is False

def test_create_access_token_looks_like_jwt():
    os.environ["JWT_SECRET_KEY"] = "test-secret"
    token = create_access_token("user@example.com")
    assert token.count(".") == 2  # header.payload.signature
