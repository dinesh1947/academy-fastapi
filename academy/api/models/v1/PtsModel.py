from sqlalchemy import Column, String, Integer, DateTime, Text, Date, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from enum import Enum as PyEnum

from .UserCourseModel import *

Base = declarative_base()

# Enum choices for role and status
class Role(PyEnum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class Status(PyEnum):
    active = "active"
    inactive = "inactive"



from typing import Optional, List
from datetime import datetime





class TestSeries(Base):
    __tablename__ = 'pts_testseries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    # goal_id = Column(Integer, ForeignKey("goal.id"), nullable=True)
    # course_type_id = Column(Integer, ForeignKey("coursetype.id"), nullable=True)
    mode = Column(String(25), nullable=True)
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    slug = Column(String(255), nullable=True)
    publish_status = Column(String(25), nullable=False)
    short_description = Column(Text, nullable=False)
    long_description = Column(Text, nullable=False)
    start_date_time = Column(DateTime, nullable=True)
    end_date_time = Column(DateTime, nullable=True)
    image = Column(String(255), nullable=True)  # store file path or URL
    url = Column(String(255), nullable=True)
    official_email = Column(String(255), nullable=True)
    test = Column(Integer, nullable=True, default=0)

    # # Relationships (optional if you need joins in ORM)
    # goal = relationship("Goal", back_populates="test_series", lazy='joined')
    # course_type = relationship("CourseType", back_populates="test_series", lazy='joined')
    # tests = relationship("Test", back_populates="test_series", lazy='joined')




class Test(Base):
    __tablename__ = 'pts_test'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    # test_series_id = Column(Integer, ForeignKey("pts_testseries.id"), nullable=False)
    duration = Column(Integer, nullable=True)  # in minutes
    # total_marks = Column(Integer, nullable=True)
    # passing_marks = Column(Integer, nullable=True)
    # start_time = Column(DateTime, nullable=True)
    # end_time = Column(DateTime, nullable=True)
    # is_active = Column(Boolean, default=True)

    # # Relationships
    # test_series = relationship("TestSeries", back_populates="tests", lazy='joined')
    # question_papers = relationship("QuestionPaper", back_populates="test")






class QuestionPaper(Base):
    __tablename__ = 'pts_questionpaper'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    # instructions = Column(Text, nullable=True)
    # total_questions = Column(Integer, nullable=True)
    # total_marks = Column(Integer, nullable=True)

 
    questions = relationship("Question", back_populates="question_paper")







class Question(Base):
    __tablename__ = 'pts_question'

    id = Column(Integer, primary_key=True, index=True)
    question_number = Column(Integer, nullable=True)
    question = Column(Text, nullable=True)
    option_a = Column(Text, nullable=True)
    option_b = Column(Text, nullable=True)
    option_c = Column(Text, nullable=True)
    option_d = Column(Text, nullable=True)
    correct_option = Column(String(25), nullable=True)  # Option A, B, C, D
    explanation = Column(Text, nullable=True)
    # language = Column(String(25), nullable=True)  # Optional: 'English', 'Hindi', etc.
    # subject = Column(Text, nullable=True)
    # difficulty_level = Column(String(25), nullable=True)
    # statement = Column(Text, nullable=True)
    # direction = Column(Text, nullable=True)
    # is_negative = Column(Boolean, default=True)  # If negative marking is applied
    # attempted_number = Column(Integer, default=0)

    # # ForeignKey and Relationship to QuestionPaper
    question_paper_id = Column(Integer, ForeignKey("pts_questionpaper.id"), nullable=False)
    question_paper = relationship("QuestionPaper", back_populates="questions")


    user_test_answers = relationship("UserTestAnswer", back_populates="question")

    # def __repr__(self):
    #     return f"<Question(id={self.id}, question_number={self.question_number})>"



















