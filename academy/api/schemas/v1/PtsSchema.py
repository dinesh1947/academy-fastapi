import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel, EmailStr
from typing import Generic, TypeVar, List, Optional, Literal
from pydantic.generics import GenericModel









class TestSeriesCreate(BaseModel):
    name: str
    mode: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    slug: Optional[str] = None
    publish_status: str
    short_description: str
    long_description: str
    start_date_time: Optional[datetime] = None
    end_date_time: Optional[datetime] = None
    image: Optional[str] = None
    url: Optional[str] = None
    official_email: Optional[str] = None
    test: Optional[int] = 0
    status: Literal["active", "inactive", "archived"] = "active"









class TestSchema(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}

    


class QuestionPaperSchema(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}







class QuestionSchema(BaseModel):
    id: int
    question_number: int
    question_paper_id: int
    question_paper: QuestionPaperSchema
    
    model_config = {"from_attributes": True}






