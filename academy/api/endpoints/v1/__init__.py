from fastapi import APIRouter

from .import user_courses, users 

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
# router.include_router(user_courses.router, prefix="/user-course", tags=["user-course"])
