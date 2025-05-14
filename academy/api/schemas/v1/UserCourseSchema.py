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


# class TestUserRead(BaseModel):
#     id: int
#     # created_at: datetime
#     # updated_at: Optional[datetime]
#     # user_course_package_id: int
#     # test_id: int
#     # # question_paper_id: Optional[int]
#     # is_agree: bool
#     # correct_answer: int
#     # incorrect_answer: int
#     # not_answer: int
#     # time_spent: int
#     # score: Optional[float]
#     # rank: Optional[int]
#     # consolidated_rank: Optional[int]
#     # test_status: str
#     # answer_mode: str
#     # start_at: Optional[datetime]
#     # end_at: Optional[datetime]
#     # restart_number: int
#     # language: str
#     # test_type: str

#     class Config:
#         orm_mode = True  
#         from_attributes=True






# class UserCoursePackageResponse(BaseModel):
#     id : int
#     user_id:Optional[int] = None
#     test_series_id :Optional[int] = None
#     course_id :Optional[int] = None
#     package_id :Optional[int] = None
#     added_by :Optional[str] = ""
#     source :Optional[str] = ""
#     rating :Optional[int] = 0
#     review_title :Optional[str] = ""
#     review :Optional[str] = ""
#     mts_id :Optional[int] = None
    

#     class Config:
#         orm_mode = True  
        
