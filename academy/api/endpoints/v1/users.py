from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import asyncio

from sqlalchemy.future import select
import hashlib


import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

print(current_dir)
print("######################################################>>>>>>^")
sys.path.insert(0, current_dir)





# from config.database import get_sync_db 
from config.database import get_async_db  
from api.endpoints.v1.utils.project_jwt import *






from api.models.v1.UserModel import *
from api.schemas.v1.UserSchema import *


router = APIRouter()







from passlib.context import CryptContext

# Create a CryptContext instance for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)




# @router.post("/login", response_model=Token)
# async def login(user: UserModel, db: Session = Depends(get_sync_db)):
#     # Fetch the user from DB using plain mobile number
#     db_user = db.query(User).filter(User.mobile == user.mobile).first()
#     hashed_password = hashlib.md5(user.password.encode()).hexdigest()
#     if not db_user or hashed_password != db_user.password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     access_token = create_access_token(data={
#         "id": db_user.id,  
#         "username": db_user.username,  
#         "mobile": db_user.mobile,  
#         "email": db_user.email,  
#         "role": db_user.role.value
#     })
#     return {"access_token": access_token, "token_type": "bearer"}



















# # from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
# # from sqlalchemy.orm import Session
# # from typing import Optional, List
# # from fastapi.responses import JSONResponse
# # from academy.app.config.database import get_sync_db, get_sync_db

# # from academy.app.api.v1.models.UserModel import User
# # from academy.app.api.v1.schemas.UserSchema import UserListSchema, UserCreateSchema, AddRegistrationMailLog
# # from academy.app.api.v1.utils.mails import SendRegistrationMailToStudents

# # router = APIRouter()



# # @router.post("/add_user", response_model=UserListSchema)
# # def add_user(user:UserCreateSchema, db:Session = Depends(get_sync_db)):
# #     u = User(name=user.name, email=user.email, password = user.password)
# #     db.add(u)
# #     db.commit()
# #     return u

# # @router.put("/update_user/{user_id}", response_model=UserListSchema)
# # def add_user(user_id:int, user:UserListSchema, db:Session=Depends(get_sync_db)):
# #     try:
# #         u = db.query(User).filter(User.id == user_id).first()
# #         u.name = user.name
# #         u.email = user.email
# #         db.add(u)
# #         db.commit()
# #         return u
# #     except:
# #         return {"code":0, "message":"user not found"}
    
# # @router.delete("/delete_user/{user_id}", response_class=JSONResponse)
# # def delete_user(user_id:int, db:Session = Depends(get_sync_db)):
# #     try:
# #         u = db.query(User).filter(User.id == user_id).first()
# #         db.delete(u)
# #         db.commit()
# #         return {"code":1, "message":f"User of id {user_id} deleted successfully"}
# #     except:
# #         return {"code":0, "message":"Getting some error please try after some time"}

    

# # @router.get("/user_list", response_model=List[UserListSchema])
# # async def all_users(db:Session = Depends(get_sync_db)):
# #     #await asyncio.sleep(1)
# #     return db.query(User).limit(100).all()

# # @router.post('/send_mail_to_registration')
# # async def approve_reject_tag_mail(reg_mail_schema: AddRegistrationMailLog, background_tasks: BackgroundTasks, db:Session=Depends(get_db)):
    
# #     background_tasks.add_task(SendRegistrationMailToStudents, reg_mail_schema, db)
# #     return {"code":1, "action":2, "message":"Mail rejected successfully"}
# #     '''if obj.status == 0:
# #         print(obj)
# #         obj.status = s
# #         obj.approved_rejected_at = func.now()
# #         db.add(obj)
# #         db.commit()

# #         if s == 1:
# #             background_tasks.add_task(SendTagListMailToStudents, id, db)
# #             background_tasks.add_task(SendListConfMailToMentor, id, db)
# #             return {"code":1, "action":1, "message":"Mail sent for approval"}
# #         else:
# #             return {"code":1, "action":2, "message":"Mail rejected successfully"}
# #     else:
# #         return {"code":0, "action":3, "message":"This link has expired"}'''
