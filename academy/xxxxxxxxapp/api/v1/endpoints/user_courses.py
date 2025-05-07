


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import asyncio
from academy.app.config.database import get_sync_db 
from academy.app.config.database import get_async_db  
from sqlalchemy.future import select
from academy.app.api.v1.utils.project_jwt import *

from academy.app.api.v1.utils.pagination import Paginator  # Import the Paginator class



from academy.app.api.v1.models.UserCourseModel import TestUser,UserCoursePackage  # SQLAlchemy model
from academy.app.api.v1.schemas.UserCourseSchema import (
    TestUserCreate,
    TestUserUpdate,
    TestUserRead,
    PaginatedResponse,
    UserCoursePackageResponse
)  


router = APIRouter()




# @router.get("/",response_model=List[TestUserRead])
# def get_test_users(db: Session = Depends(get_sync_db)):
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     try:
#         # Fetch test users from the database
#         # test_users = db.query(TestUser).all()
#         test_users = db.query(TestUser).order_by(TestUser.id).limit(10).all()
#         return test_users
#     except Exception as e:
#         # Handle exceptions (e.g., database errors)
#         print(f"Error fetching test users: {e}")
#         raise HTTPException(status_code=500, detail="Error fetching test users")







@router.get("/", response_model=List[TestUserRead])
def get_test_users(db: Session = Depends(get_sync_db), current_user: User = Depends(get_current_user_sync) ):
    try:
        print("**********************>>>>>>>>>")
        # Fetch test users from the database synchronously
        test_users = db.query(TestUser).order_by(TestUser.id).limit(10).all()
        return test_users
    except Exception as e:
        # Handle exceptions (e.g., database errors)
        print(f"Error fetching test users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching test users")





@router.get("/all-test/", response_model=List[UserCoursePackageResponse])
def get_all_test(db: Session = Depends(get_sync_db), current_user: User = Depends(get_current_user_sync) ):
    try:
        print("**********************>>>>>>>>>")
        print(current_user)
        print(type(current_user))
        print(current_user.id)
        print("###################################################################")
        # Fetch test users from the database synchronously
        # ucp = db.query(UserCoursePackage).order_by(UserCoursePackage.id).limit(10).all()
        # ucp = db.query(UserCoursePackage).filter(UserCoursePackage.user_id == current_user.id).order_by(UserCoursePackage.id).limit(10).all()
        ucp = db.query(UserCoursePackage).filter(UserCoursePackage.user_id == current_user.id).filter(UserCoursePackage.test_series_id.isnot(None))
        return ucp
    except Exception as e:
        # Handle exceptions (e.g., database errors)
        print(f"Error fetching test users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching test users")










@router.get("/list", response_model=PaginatedResponse)
def get_test_users(
    db: Session = Depends(get_sync_db),
    current_user: User = Depends(get_current_user_sync),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    try:
        base_url="http://127.0.0.1:8000/api/v1/user-course/list"
        paginator = Paginator(db=db, model=TestUser, pydantic_model=TestUserRead,base_url=base_url,page=page, page_size=page_size)
        response = paginator.get_paginated_response()        
        # print("Paginated Response:", response)  # Check the structure of the response
        return response

    except HTTPException as e:
        print(f"Authentication failed: {e.detail}")
        raise e  # Re-raise the authentication error

    except Exception as e:
        print(f"Error fetching test users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching test users")











@router.get("/async/", response_model=List[TestUserRead])
async def get_first_and_last_test_users(db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user_async)):

    first_query = select(TestUser).order_by(TestUser.id).limit(10)
    last_query = select(TestUser).order_by(TestUser.id.desc()).limit(10)

    first_result, last_result = await asyncio.gather(
        db.execute(first_query),
        db.execute(last_query)
    )

    first_test_users = first_result.scalars().all()
    last_test_users = list(reversed(last_result.scalars().all()))

    return first_test_users + last_test_users

















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





