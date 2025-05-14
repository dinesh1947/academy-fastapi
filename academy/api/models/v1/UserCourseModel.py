from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float,DateTime, SmallInteger,UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship



Base = declarative_base()






# class UserCoursePackage(Base):
#     __tablename__ = "user_courses_usercoursepackage"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer)
#     test_series_id = Column(Integer)
#     course_id = Column(Integer)
#     package_id = Column(Integer)
#     added_by =Column(String, default="Online")
#     source = Column(String,  default="admin panel")
#     rating = Column(Integer, default=0)
#     review_title = Column(String,  default="")
#     review = Column(String,  default="")
#     mts_id = Column(Integer)
    















class UserTest(Base):
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
    answers = relationship("UserTestAnswer", back_populates="user_test", cascade="all, delete-orphan")







class UserTestAnswer(Base):
    __tablename__ = "user_test_answer"
    __table_args__ = (
        UniqueConstraint("user_test_id", "question_number", name="uq_user_test_question_number"),
    )

    id = Column(Integer, primary_key=True, index=True)
    question_paper_id = Column(Integer, ForeignKey("question_paper.id", ondelete="SET NULL"), nullable=True)
    question_id = Column(Integer, ForeignKey("question.id", ondelete="SET NULL"), nullable=True)

    question_number = Column(SmallInteger, nullable=True)
    answer = Column(String(20), nullable=True, default='')
    is_correct = Column(Integer, nullable=True, default=0)
    score_status = Column(Integer, nullable=True, default=0)
    mark_for_review = Column(Boolean, default=False)
    respond_at = Column(DateTime, nullable=True)
    how_sure = Column(String(4), nullable=True)





    user_test_id = Column(Integer,ForeignKey("user_courses_usertest.id", ondelete="CASCADE"),nullable=False)
    user_test = relationship("UserTest", back_populates="answers")