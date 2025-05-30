# api/models/v1/UserCourseModel.py

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, SmallInteger, UniqueConstraint, ForeignKey, Text, Float

from .base import Base

if TYPE_CHECKING:
    from .PtsModel import Question  # for type hint only










class UserCoursePackage(Base):
    __tablename__ = 'user_courses_usercoursepackage'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=False)
    test_series_id: Mapped[int | None] = mapped_column(Integer, nullable=False)
    course_id: Mapped[int | None] = mapped_column(Integer, nullable=False)
    package_id: Mapped[int | None] = mapped_column(Integer, nullable=False)
    mts_id: Mapped[int | None] = mapped_column(Integer, nullable=False)
    added_by: Mapped[str | None] = mapped_column(String(255), nullable=True, default="Online")
    source: Mapped[str | None] = mapped_column(String(255), nullable=True, default="admin panel")
    rating: Mapped[int] = mapped_column(Integer, default=0)
    review_title: Mapped[str | None] = mapped_column(String(25), nullable=True, default='')
    review: Mapped[str | None] = mapped_column(Text, nullable=True, default='')
    show_status: Mapped[str | None] = mapped_column(String(250), nullable=True, default="start")
    is_recommended: Mapped[bool] = mapped_column(Boolean, default=False)











class UserTest(Base):
    __tablename__ = "user_courses_usertest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None)

    user_course_package_id: Mapped[int] = mapped_column(Integer, nullable=False)
    test_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    question_paper_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    is_agree: Mapped[bool] = mapped_column(Boolean, default=False)
    correct_answer: Mapped[int] = mapped_column(Integer, default=0)
    incorrect_answer: Mapped[int] = mapped_column(Integer, default=0)
    not_answer: Mapped[int] = mapped_column(Integer, default=0)
    time_spent: Mapped[int] = mapped_column(Integer, default=0)

    score: Mapped[Optional[float]] = mapped_column(Float, default=None)
    rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    consolidated_rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    test_status: Mapped[str] = mapped_column(String(50), default="start")
    answer_mode: Mapped[str] = mapped_column(String(50), default="web")

    start_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    restart_number: Mapped[int] = mapped_column(Integer, default=0)
    language: Mapped[str] = mapped_column(String(50), default="")
    test_type: Mapped[str] = mapped_column(String(50), default="pts")

    # Use string reference to avoid circular import
    answers: Mapped[List["UserTestAnswer"]] = relationship(
        "UserTestAnswer",
        back_populates="user_test",
        cascade="all, delete-orphan"
    )






class UserTestAnswer(Base):
    __tablename__ = "user_courses_usertestanswer"
    __table_args__ = (
        UniqueConstraint("user_test_id", "question_number", name="uq_user_test_question_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    question_number: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    answer: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default='')
    is_correct: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    score_status: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    mark_for_review: Mapped[bool] = mapped_column(Boolean, default=False)
    respond_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    how_sure: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)

    user_test_id: Mapped[int] = mapped_column(ForeignKey("user_courses_usertest.id", ondelete="CASCADE"), nullable=False)
    user_test: Mapped["UserTest"] = relationship("UserTest", back_populates="answers")

    question_id: Mapped[Optional[int]] = mapped_column(ForeignKey("pts_question.id", ondelete="SET NULL"))
    question: Mapped[Optional["Question"]] = relationship("Question", back_populates="user_test_answers")
