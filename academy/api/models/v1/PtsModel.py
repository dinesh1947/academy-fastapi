# api/models/v1/PtsModel.py

from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .UserCourseModel import UserTestAnswer


class Role(PyEnum):
    student = "student"
    teacher = "teacher"
    admin = "admin"


class Status(PyEnum):
    active = "active"
    inactive = "inactive"


class TestSeries(Base):
    __tablename__ = 'pts_testseries'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    mode: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    slug: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    publish_status: Mapped[str] = mapped_column(String(25), nullable=False)
    short_description: Mapped[str] = mapped_column(Text, nullable=False)
    long_description: Mapped[str] = mapped_column(Text, nullable=False)
    start_date_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    official_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    test: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)


class Test(Base):
    __tablename__ = 'pts_test'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mark_per_right: Mapped[float] = mapped_column(Float, default=1.00)
    mark_per_wrong: Mapped[float] = mapped_column(Float, default=1.00)


    question_paper_id: Mapped[int] = mapped_column(ForeignKey("pts_questionpaper.id"), nullable=False)
    question_paper: Mapped["QuestionPaper"] = relationship("QuestionPaper", back_populates="test")




class QuestionPaper(Base):
    __tablename__ = 'pts_questionpaper'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    

    test: Mapped[List["Test"]] = relationship("Test", back_populates="question_paper")
    questions: Mapped[List["Question"]] = relationship("Question", back_populates="question_paper")


class Question(Base):
    __tablename__ = 'pts_question'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    question: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    option_a: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    option_b: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    option_c: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    option_d: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    correct_answer: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    incorrect_answer: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    not_answer: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


    correct_option: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    question_paper_id: Mapped[int] = mapped_column(ForeignKey("pts_questionpaper.id"), nullable=False)
    question_paper: Mapped["QuestionPaper"] = relationship("QuestionPaper", back_populates="questions")

    # Use string refs to avoid import loop
    user_test_answers: Mapped[List["UserTestAnswer"]] = relationship("UserTestAnswer", back_populates="question")








