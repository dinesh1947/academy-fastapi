# main.py
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, current_dir)

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import traceback
from sqlalchemy.orm import Session
from config.database import get_async_db
import asyncio

from api.endpoints.v1 import router as v1_router



import jwt
from exception_handlers import jwt_expired_handler, jwt_invalid_token_handler, global_exception_handler,not_authenticated_handler



app = FastAPI()

app.include_router(v1_router , prefix="/api")


app.add_exception_handler(jwt.ExpiredSignatureError, jwt_expired_handler)
app.add_exception_handler(jwt.InvalidTokenError, jwt_invalid_token_handler)
app.add_exception_handler(HTTPException, not_authenticated_handler)  # Handle Not Authenticated
app.add_exception_handler(Exception, global_exception_handler)




# @app.get("/check-connections")
# async def check_connections(sync_db: Session = Depends(get_sync_db)):
#     """
#     Check if both synchronous and asynchronous database connections are successful.
#     """
#     # Check synchronous connection
#     try:
#         sync_result = sync_db.execute("SELECT 1").fetchone()
#         sync_status = True if sync_result else False
#     except Exception as e:
#         sync_status = False

#     # Check asynchronous connection
#     try:
#         query = "SELECT 1"
#         async_result = await async_database.fetch_one(query=query)
#         async_status = True if async_result else False
#     except Exception as e:
#         async_status = False

#     if not sync_status or not async_status:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     return {
#         "sync_connection": sync_status,
#         "async_connection": async_status
#     }




# # Optionally, you can add a route to perform database testing explicitly for debugging purposes.
# # @app.get("/test-connections")
# # def test_connections():
# #     """
# #     Test both synchronous and asynchronous connections directly.
# #     """
# #     # Test synchronous connection
# #     try:
# #         sync_result = sync_db.execute("SELECT 1").fetchone()
# #         sync_status = True if sync_result else False
# #     except Exception as e:
# #         sync_status = False

# #     # Test asynchronous connection
# #     async def async_test():
# #         try:
# #             query = "SELECT 1"
# #             async_result = await async_database.fetch_one(query=query)
# #             async_status = True if async_result else False
# #         except Exception as e:
# #             async_status = False
# #         return async_status

# #     async_status = asyncio.run(async_test())

# #     if not sync_status or not async_status:
# #         raise HTTPException(status_code=500, detail="Database connection failed")

# #     return {
# #         "sync_connection": sync_status,
# #         "async_connection": async_status
# #     }
