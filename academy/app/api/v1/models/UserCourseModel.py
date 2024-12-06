from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class TestUser(Base):
    __tablename__ = "user_courses_usertest"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None)
    user_course_package_id = Column(Integer)
    test_id = Column(Integer)
    question_paper_id = Column(Integer, nullable=True)
    is_agree = Column(Boolean, default=False)
    correct_answer = Column(Integer, default=0)
    incorrect_answer = Column(Integer, default=0)
    not_answer = Column(Integer, default=0)
    time_spent = Column(Integer, default=0)
    score = Column(Float, default=None)
    rank = Column(Integer, nullable=True)
    consolidated_rank = Column(Integer, nullable=True)
    test_status = Column(String, default="start")
    answer_mode = Column(String, default="web")
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)
    restart_number = Column(Integer, default=0)
    language = Column(String, default="")
    test_type = Column(String, default="pts")
