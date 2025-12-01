from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from .config import get_jwt_secret_key, get_jwt_algorithm, get_jwt_expire_minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=get_jwt_expire_minutes())
    payload = {"sub": subject, "iat": int(now.timestamp()), "exp": exp}
    return jwt.encode(payload, get_jwt_secret_key(), algorithm=get_jwt_algorithm())
