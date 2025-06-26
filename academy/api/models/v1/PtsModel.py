# api/models/v1/PtsModel.py

from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Float, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from sqlalchemy import Enum as SqlEnum

from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum


from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .UserCourseModel import UserTestAnswer

import math


# if TYPE_CHECKING:
#     from .UserModel import User




class Role(PyEnum):
    student = "student"
    teacher = "teacher"
    admin = "admin"


class Status(PyEnum):
    active = "active"
    inactive = "inactive"

STATUS = ("active", "inactive", "archived")


class LanguageEnum(str, Enum):
    english = "english"
    hindi = "hindi"





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
    # image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    

    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    official_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    test: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    status: Mapped[str] = mapped_column(SqlEnum(*STATUS, name="status_enum"), default="active", nullable=False)





    # created_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)
    # updated_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)

    # created_by: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by_id], backref="testseries_created_by")
    # updated_by: Mapped[Optional["User"]] = relationship("User", foreign_keys=[updated_by_id], backref="testseries_updated_by")






class Test(Base):
    __tablename__ = 'pts_test'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(40), unique=True)

    question_paper_id: Mapped[Optional[int]] = mapped_column(ForeignKey("pts_questionpaper.id"), nullable=True)

    instruction: Mapped[Optional[str]] = mapped_column(Text, default='', nullable=True)
    hindi_instruction: Mapped[Optional[str]] = mapped_column(Text, default='', nullable=True)

    schedule_date_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    mark_per_right: Mapped[float] = mapped_column(Float, default=1.00)
    mark_per_wrong: Mapped[float] = mapped_column(Float, default=1.00)

    is_quiz: Mapped[bool] = mapped_column(Boolean, default=False)
    test_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Assuming storing file path

    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=1)
    total_question: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)

    offline_virtual_rank: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=1.0)
    online_virtual_rank: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=1.0)

    restart_number: Mapped[Optional[int]] = mapped_column(Integer, default=3)
    change_numerator: Mapped[bool] = mapped_column(Boolean, default=False)

    test_type: Mapped[Optional[str]] = mapped_column(String(25), default="pts")  # or use Enum if needed

        
    @property
    def maximum_marks(self):
        if self.mark_per_right is None or self.total_question is None:
            return 0
        return math.ceil(self.mark_per_right * self.total_question)







class TestPackage(Base):
    __tablename__ = "pts_testpackage"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    test_id: Mapped[int] = mapped_column(Integer, nullable=True)
    package_id: Mapped[int] = mapped_column(Integer, nullable=True)
    start_date_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)




class QuestionPaper(Base):
    __tablename__ = 'pts_questionpaper'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    




class Question(Base):
    __tablename__ = 'pts_question'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    question_paper_id: Mapped[int] = mapped_column(Integer, ForeignKey("pts_questionpaper.id"), nullable=False)
    question_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    question: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    option_a: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    option_b: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    option_c: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    option_d: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    correct_option: Mapped[Optional[str]] = mapped_column(String(25), nullable=True, default="")
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


    language: Mapped[Optional[LanguageEnum]] = mapped_column(SQLAlchemyEnum(LanguageEnum, name="language_enum"), nullable=True )

    correct_answer: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    incorrect_answer: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    not_answer: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)

    source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")
    subject_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")
    topic: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")
    topic_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")
    sub_topic: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")
    sub_topic_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")

    difficulty_level: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    statement: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    direction: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")
    is_negative: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)

    attempted_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)



