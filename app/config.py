import os

def get_env(name: str, default: str) -> str:
    val = os.getenv(name)
    return val if val not in (None, "") else default

def get_database_url() -> str:
    return get_env("DATABASE_URL", "sqlite:///./app.db")

def get_jwt_secret_key() -> str:
    return get_env("JWT_SECRET_KEY", "dev-secret-change-me")

def get_jwt_algorithm() -> str:
    return get_env("JWT_ALGORITHM", "HS256")

def get_jwt_expire_minutes() -> int:
    return int(get_env("JWT_EXPIRE_MINUTES", "60"))
