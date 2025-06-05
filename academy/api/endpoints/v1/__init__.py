from fastapi import APIRouter

from .import  users
from .import  user_courses
from .import  pts

router = APIRouter()

router.include_router(users.router, prefix="/v1/user", tags=["users"])
router.include_router(user_courses.router, prefix="/v1/user-course", tags=["user-course"])
router.include_router(pts.router, prefix="/v1/pts", tags=["pts"])
