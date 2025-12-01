from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# Ensure models are imported so tables exist in metadata
from app import models  # noqa: F401


@pytest.fixture()
def client(tmp_path: Path):
    # Use an isolated in-memory SQLite DB per test
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_root_redirects_to_login(client: TestClient):
    r = client.get("/", allow_redirects=False)
    assert r.status_code in (302, 307)
    assert r.headers["location"].endswith("/static/login.html")


def test_register_success_returns_token(client: TestClient):
    r = client.post("/register", json={"email": "a1@example.com", "password": "StrongPass123!"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert "access_token" in data and data["access_token"]
    assert data["token_type"] == "bearer"
    assert data["access_token"].count(".") == 2


def test_register_duplicate_returns_400(client: TestClient):
    payload = {"email": "dup@example.com", "password": "StrongPass123!"}
    r1 = client.post("/register", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/register", json=payload)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Email already registered"


def test_register_invalid_email_422(client: TestClient):
    r = client.post("/register", json={"email": "not-an-email", "password": "StrongPass123!"})
    assert r.status_code == 422


def test_register_short_password_422(client: TestClient):
    r = client.post("/register", json={"email": "short@example.com", "password": "short"})
    assert r.status_code == 422


def test_login_success_returns_token(client: TestClient):
    client.post("/register", json={"email": "login@example.com", "password": "StrongPass123!"})
    r = client.post("/login", json={"email": "login@example.com", "password": "StrongPass123!"})
    assert r.status_code == 200, r.text
    assert "access_token" in r.json()
    assert r.json()["access_token"].count(".") == 2


def test_login_unknown_user_returns_401(client: TestClient):
    r = client.post("/login", json={"email": "nouser@example.com", "password": "StrongPass123!"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid credentials"


def test_login_wrong_password_returns_401(client: TestClient):
    client.post("/register", json={"email": "wrong@example.com", "password": "StrongPass123!"})
    r = client.post("/login", json={"email": "wrong@example.com", "password": "BadPass"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid credentials"
