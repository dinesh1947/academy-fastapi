from sqlalchemy import Column, Integer, Boolean, Float, String, DateTime, ForeignKey
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from typing import List




class UserTestSchema(BaseModel):
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

    model_config = {"from_attributes": True}



class QuestionSchema(BaseModel):
    id: int
    question_number: int  
    correct_option: str  

    model_config = {"from_attributes": True}



class UserTestAnswerSchema(BaseModel):
    id: int
    question_number: int
    answer: str
    is_correct: int
    question_id: int
    question: Optional[QuestionSchema]
    model_config = {"from_attributes": True}





class StartTestSchema(BaseModel):
    ucp_id: Optional[int] = None
    test_id: int = Field(..., description="ID of the test to start")
    answer_mode: Optional[str] = "web"
    test_type: Optional[str] = "pts"


class AgreeTestSchema(BaseModel):
    user_test_id: Optional[int] = None  
    is_agree: bool = False              
    language: Optional[str] = "english" 




