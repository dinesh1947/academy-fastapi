from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TestUser(BaseModel):
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
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

    class Config:
        orm_mode = True  
