from app.config.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, func, Date

class User(Base):
    __tablename__ = 'user'
    id=Column(Integer, primary_key=True, index=True)
    userName=Column(String(255))
    fullName=Column(String(255))
    email=Column(String(255))
    phone=Column(String(20))
    roll_number=Column(String(20))
    password=Column(String(255))
    joinDate=Column(DateTime)

class RegistrationMailLog(Base):
    __tablename__ = 'registration_mail_logs'
    id=Column(Integer, primary_key=True, index=True)
    agent_id=Column(Integer)
    subject = Column(String(255))
    body = Column(Text)
    mail_sent_to = Column(Text)
    status = Column(Integer)
    registration_date=Column(Date, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())