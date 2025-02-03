from sqlalchemy import Column, Integer, Boolean, Float, String, DateTime, ForeignKey
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from typing import List




# Shared properties
class TestUserBase(BaseModel):
    user_course_package_id: int
    test_id: int
    question_paper_id: Optional[int] = None
    is_agree: bool = False
    correct_answer: Optional[int] = Field(default=0, ge=0)
    incorrect_answer: Optional[int] = Field(default=0, ge=0)
    not_answer: Optional[int] = Field(default=0, ge=0)
    time_spent: Optional[int] = Field(default=0, ge=0)
    score: Optional[float] = Field(default=None, le=999.99)
    rank: Optional[int] = None
    consolidated_rank: Optional[int] = None
    test_status: str = "start"
    answer_mode: str = "web"
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    restart_number: Optional[int] = Field(default=0, ge=0)
    language: Optional[str] = ""
    test_type: Optional[str] = "pts"

# Schema for creating a new TestUser
class TestUserCreate(TestUserBase):
    pass

# Schema for updating an existing TestUser
class TestUserUpdate(TestUserBase):
    pass

# Schema for reading a TestUser
class TestUserRead(BaseModel):
    id: int


    class Config:
        orm_mode = True



from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TestUserRead(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    user_course_package_id: int
    test_id: int
    question_paper_id: Optional[int]
    is_agree: bool
    correct_answer: int
    incorrect_answer: int
    not_answer: int
    time_spent: int
    score: Optional[float]
    rank: Optional[int]
    consolidated_rank: Optional[int]
    test_status: str
    answer_mode: str
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    restart_number: int
    language: str
    test_type: str

    class Config:
        orm_mode = True  
        from_attributes=True



class PaginatedResponse(BaseModel):
    total_count: int
    page: int
    page_size: int
    total_pages: int
    results: List[TestUserRead]