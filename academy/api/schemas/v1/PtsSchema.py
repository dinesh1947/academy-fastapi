import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional
from pydantic.generics import GenericModel





class TestSchema(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}

    




class QuestionPaperSchema(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}






