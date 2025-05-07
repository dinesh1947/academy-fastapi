from app.config.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional

from app.api.v1.models.UserModel import User


class BookingTags(Base):
    __tablename__ = 'bookings_tags'
    id=Column(Integer, primary_key=True, index=True)
    tag_name=Column(String(255))
    addedBy = Column(Integer)
    created_date = Column(DateTime)

class BookingTagStudent(Base):
    __tablename__ = 'bookings_student_tags'
    id=Column(Integer, primary_key=True, index=True)
    student_id=Column(Integer, ForeignKey('user.id'))
    tag_id = Column(Integer)
    addedBy = Column(Integer)
    created_at = Column(DateTime)
    student = relationship("User")

class BookingTagMail(Base):
    __tablename__ = 'booking_tag_mails'
    id=Column(Integer, primary_key=True, index=True)
    to_tags=Column(String(255))
    avoid_tags = Column(String(255))
    subject = Column(String(255))
    body = Column(Text)
    mentor_id=Column(Integer)
    manager_id = Column(Integer)
    status = Column(Integer)
    student_ids = Column(String(255), nullable=True) 
    approved_rejected_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())