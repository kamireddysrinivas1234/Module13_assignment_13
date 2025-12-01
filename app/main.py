from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .schemas import RegisterRequest, LoginRequest, TokenResponse
from .crud import get_user_by_email, create_user
from .security import hash_password, verify_password, create_access_token

app = FastAPI(title="JWT Auth + Frontend + Playwright + Pytest")

# Create tables (simple approach for assignments)
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/static/login.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(payload.password)
    create_user(db, payload.email, hashed)

    token = create_access_token(subject=payload.email.lower())
    return TokenResponse(access_token=token)

@app.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token)
