from enum import Enum as PyEnum
from typing import Optional
from datetime import date, datetime

from sqlalchemy import (
    String, Integer, DateTime, Text, Date, Boolean, Enum, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# SQLAlchemy 2.0 base class
class Base(DeclarativeBase):
    pass


# Enum choices for role and status
class Role(PyEnum):
    student = "student"
    teacher = "teacher"
    admin = "admin"
    instructor = "instructor"


class Status(PyEnum):
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    mobile: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    rollnumber: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    forum_email: Mapped[Optional[str]] = mapped_column(String(255))
    source: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.student, nullable=False)
    status: Mapped[int] = mapped_column(nullable=False)


class RegistrationMailLog(Base):
    __tablename__ = 'registration_mail_logs'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    agent_id: Mapped[int] = mapped_column(nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    mail_sent_to: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[int] = mapped_column(nullable=False)
    registration_date: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<RegistrationMailLog(agent_id={self.agent_id}, status={self.status})>"
