from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from academy.app.api.v1.models.UserCourseModel import TestUser  # SQLAlchemy model
from academy.app.api.v1.schemas.UserCourseSchema import (
    TestUserCreate,
    TestUserUpdate,
    TestUserRead,
)  # Pydantic schemas for TestUser
from academy.app.config.database import get_sync_db  # Dependency for DB session

router = APIRouter()

# Fetch all TestUsers
@router.get("/", response_model=List[TestUserRead])
def get_test_users(db: Session = Depends(get_sync_db)):
    """
    Fetch all TestUser records.
    """
    test_users = db.query(TestUser).all()
    return test_users

# Fetch a single TestUser by ID
@router.get("/{test_user_id}", response_model=TestUserRead)
def get_test_user(test_user_id: int, db: Session = Depends(get_sync_db)):
    """
    Fetch a single TestUser by its ID.
    """
    test_user = db.query(TestUser).filter(TestUser.id == test_user_id).first()
    if not test_user:
        raise HTTPException(status_code=404, detail="TestUser not found")
    return test_user

# Create a new TestUser
@router.post("/", response_model=TestUserRead)
def create_test_user(test_user: TestUserCreate, db: Session = Depends(get_sync_db)):
    """
    Create a new TestUser record.
    """
    new_test_user = TestUser(**test_user.dict())
    db.add(new_test_user)
    db.commit()
    db.refresh(new_test_user)
    return new_test_user

# Update an existing TestUser by ID
@router.put("/{test_user_id}", response_model=TestUserRead)
def update_test_user(
    test_user_id: int, test_user: TestUserUpdate, db: Session = Depends(get_sync_db)
):
    """
    Update an existing TestUser by its ID.
    """
    existing_test_user = db.query(TestUser).filter(TestUser.id == test_user_id).first()
    if not existing_test_user:
        raise HTTPException(status_code=404, detail="TestUser not found")
    for key, value in test_user.dict(exclude_unset=True).items():
        setattr(existing_test_user, key, value)
    db.commit()
    db.refresh(existing_test_user)
    return existing_test_user

# Delete a TestUser by ID
@router.delete("/{test_user_id}", response_model=dict)
def delete_test_user(test_user_id: int, db: Session = Depends(get_sync_db)):
    """
    Delete a TestUser by its ID.
    """
    test_user = db.query(TestUser).filter(TestUser.id == test_user_id).first()
    if not test_user:
        raise HTTPException(status_code=404, detail="TestUser not found")
    db.delete(test_user)
    db.commit()
    return {"message": "TestUser deleted successfully"}
