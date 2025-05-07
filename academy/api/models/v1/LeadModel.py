from sqlalchemy import Column, String, Integer, DateTime, Text, func, ForeignKey, Date, Time, SmallInteger
from sqlalchemy.orm import relationship
from typing import Optional

from config.database import Base

class Counselling(Base):
    __tablename__ = 'schedules'
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer)
    agent_id=Column(Integer, nullable=True)
    assigned_by=Column(Integer, nullable=True)
    cancel_by=Column(Integer, nullable=True)
    fullName=Column(String(255))
    email=Column(String(255))
    phone=Column(String(15))
    reason=Column(Text)
    schedule_date=Column(Date)
    schedule_time=Column(Time)
    status=Column(SmallInteger)
    submitDate = Column(DateTime, server_default=func.now())
