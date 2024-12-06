from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
class TestUserRead(TestUserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
