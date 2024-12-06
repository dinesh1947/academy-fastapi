# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from academy.app.config.database import get_sync_db, async_database
import asyncio


from academy.app.api.v1.endpoints import user_courses

app = FastAPI()
app.include_router(user_courses.router, prefix="/api/v1/test_users", tags=["TestUsers"])

@app.get("/")
def read_root():
    return {"Hello": "This Code Is Deployed To Server Using Jenkins Pipeline"}

@app.get("/check-connections")
async def check_connections(sync_db: Session = Depends(get_sync_db)):
    """
    Check if both synchronous and asynchronous database connections are successful.
    """
    # Check synchronous connection
    try:
        sync_result = sync_db.execute("SELECT 1").fetchone()
        sync_status = True if sync_result else False
    except Exception as e:
        sync_status = False

    # Check asynchronous connection
    try:
        query = "SELECT 1"
        async_result = await async_database.fetch_one(query=query)
        async_status = True if async_result else False
    except Exception as e:
        async_status = False

    if not sync_status or not async_status:
        raise HTTPException(status_code=500, detail="Database connection failed")

    return {
        "sync_connection": sync_status,
        "async_connection": async_status
    }

# Optionally, you can add a route to perform database testing explicitly for debugging purposes.
# @app.get("/test-connections")
# def test_connections():
#     """
#     Test both synchronous and asynchronous connections directly.
#     """
#     # Test synchronous connection
#     try:
#         sync_result = sync_db.execute("SELECT 1").fetchone()
#         sync_status = True if sync_result else False
#     except Exception as e:
#         sync_status = False

#     # Test asynchronous connection
#     async def async_test():
#         try:
#             query = "SELECT 1"
#             async_result = await async_database.fetch_one(query=query)
#             async_status = True if async_result else False
#         except Exception as e:
#             async_status = False
#         return async_status

#     async_status = asyncio.run(async_test())

#     if not sync_status or not async_status:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     return {
#         "sync_connection": sync_status,
#         "async_connection": async_status
#     }
