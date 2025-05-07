import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel
from typing import List


#
# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Pydantic Models
class TestSchema(BaseModel):
    id: int
    name: str







class PaginatedResponse(BaseModel):
    total_count: int
    page: int
    page_size: int
    total_pages: int
    first: Optional[str] = None
    last: Optional[str] = None
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[TestSchema]







# class UserInDB(UserModel):
#     hashed_password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str




# class CurrentUser(BaseModel):
#     id: int
#     username: str
#     email: str
#     rollnumber: str

#     class Config:
#         from_attributes = True  # This enables ORM mode