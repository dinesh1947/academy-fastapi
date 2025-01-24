from fastapi import APIRouter

# from .endpoints import items, users, bookings, leads
from .endpoints import user_courses

router = APIRouter()

# router.include_router(items.router, prefix="/items", tags=["items"])
# router.include_router(users.router, prefix="/users", tags=["users"])
# router.include_router(bookings.router, prefix="/booking", tags=["bookings"])
# router.include_router(leads.router, prefix="/lead", tags=["lead"])
router.include_router(user_courses.router, prefix="/user-course", tags=["user-course"])