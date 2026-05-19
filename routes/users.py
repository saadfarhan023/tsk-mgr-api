from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import get_session
from auth import hash_password, verify_password, create_access_token
from models import User
from typing import Dict, Any

router = APIRouter(prefix="/users", tags=["users"])


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(
    body: RegisterRequest, session: Session = Depends(get_session)
) -> Dict[str, Any]:
    existing = session.exec(select(User).where(User.email == body.email)).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=body.email, hashed_password=hash_password(body.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "email": user.email}


@router.post("/login")
def login(body: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == body.email)).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
