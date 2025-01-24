from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import List

# Import database session and models
from academy.app.config.database import get_sync_db
from academy.app.api.v1.models.UserModel import User
from academy.app.api.v1.schemas.UserSchema import *

# Secret key and algorithm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Dependency to extract the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to decode and verify the JWT token
def verify_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Database query function to fetch the user by ID
def get_user_by_id_sync(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Function to verify the token and fetch the current user
def verify_token_sync(db: Session, token: str):
    payload = verify_access_token(token)
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: User ID missing")
    return get_user_by_id_sync(db, user_id)

# Dependency to get the current user
def get_current_user_sync(db: Session = Depends(get_sync_db), token: str = Depends(oauth2_scheme)):
    return verify_token_sync(db, token)

