from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi.responses import JSONResponse
from app.config.database import get_db, get_db2

from app.api.v1.models.UserModel import User
from app.api.v1.schemas.UserSchema import UserListSchema, UserCreateSchema, AddRegistrationMailLog
from app.api.v1.utils.mails import SendRegistrationMailToStudents

router = APIRouter()



@router.post("/add_user", response_model=UserListSchema)
def add_user(user:UserCreateSchema, db:Session = Depends(get_db)):
    u = User(name=user.name, email=user.email, password = user.password)
    db.add(u)
    db.commit()
    return u

@router.put("/update_user/{user_id}", response_model=UserListSchema)
def add_user(user_id:int, user:UserListSchema, db:Session=Depends(get_db)):
    try:
        u = db.query(User).filter(User.id == user_id).first()
        u.name = user.name
        u.email = user.email
        db.add(u)
        db.commit()
        return u
    except:
        return {"code":0, "message":"user not found"}
    
@router.delete("/delete_user/{user_id}", response_class=JSONResponse)
def delete_user(user_id:int, db:Session = Depends(get_db)):
    try:
        u = db.query(User).filter(User.id == user_id).first()
        db.delete(u)
        db.commit()
        return {"code":1, "message":f"User of id {user_id} deleted successfully"}
    except:
        return {"code":0, "message":"Getting some error please try after some time"}

    

@router.get("/user_list", response_model=List[UserListSchema])
async def all_users(db:Session = Depends(get_db2)):
    #await asyncio.sleep(1)
    return db.query(User).limit(100).all()

@router.post('/send_mail_to_registration')
async def approve_reject_tag_mail(reg_mail_schema: AddRegistrationMailLog, background_tasks: BackgroundTasks, db:Session=Depends(get_db)):
    
    background_tasks.add_task(SendRegistrationMailToStudents, reg_mail_schema, db)
    return {"code":1, "action":2, "message":"Mail rejected successfully"}
    '''if obj.status == 0:
        print(obj)
        obj.status = s
        obj.approved_rejected_at = func.now()
        db.add(obj)
        db.commit()

        if s == 1:
            background_tasks.add_task(SendTagListMailToStudents, id, db)
            background_tasks.add_task(SendListConfMailToMentor, id, db)
            return {"code":1, "action":1, "message":"Mail sent for approval"}
        else:
            return {"code":1, "action":2, "message":"Mail rejected successfully"}
    else:
        return {"code":0, "action":3, "message":"This link has expired"}'''
