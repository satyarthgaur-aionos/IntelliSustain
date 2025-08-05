from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
from typing import Optional

from database import SessionLocal
from user_model import User

# 🔐 Security config
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-key")  # Make sure to override this in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔒 Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🔑 Hash password
def get_password_hash(password: str):
    return pwd_context.hash(password)

# ✅ Compare password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 🔐 JWT Token generator
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔍 Get user from DB
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# ✅ Verify user login
def verify_user(email: str, password: str):
    db = SessionLocal()
    try:
        user = get_user_by_email(db, email)
        if user is not None and user.hashed_password is not None:
            if verify_password(password, str(user.hashed_password)):
                return user
        return None
    finally:
        db.close()

# 🧑‍💼 Get current user from JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = SessionLocal()
    try:
        user = get_user_by_email(db, email)
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close()
