from typing import Optional
from sqlalchemy.orm import Session
from .models import User

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email.lower()).first()

def create_user(db: Session, email: str, hashed_password: str) -> User:
    user = User(email=email.lower(), hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
