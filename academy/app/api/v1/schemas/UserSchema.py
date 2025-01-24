import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel

# Secret key and algorithm for JWT
SECRET_KEY = "your-secret-key"  # Replace with a more secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Pydantic Models
class UserModel(BaseModel):
    mobile: str
    password: str

class UserInDB(UserModel):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

