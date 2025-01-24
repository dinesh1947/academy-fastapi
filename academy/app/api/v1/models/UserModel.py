from sqlalchemy import Column, String, Integer, DateTime, Text, Date, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from enum import Enum as PyEnum

Base = declarative_base()

# Enum choices for role and status
class Role(PyEnum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class Status(PyEnum):
    active = "active"
    inactive = "inactive"

# SQLAlchemy User model (converted from Django model)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    mobile = Column(String(20), unique=True, nullable=False)
    rollnumber = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    forum_email = Column(String(255), nullable=True)
    source = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    
    
 




# SQLAlchemy RegistrationMailLog model (converted from Django model)
class RegistrationMailLog(Base):
    __tablename__ = 'registration_mail_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    mail_sent_to = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)
    registration_date = Column(Date, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<RegistrationMailLog(agent_id={self.agent_id}, status={self.status})>"
