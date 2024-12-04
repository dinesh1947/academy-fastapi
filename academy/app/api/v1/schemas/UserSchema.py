from pydantic import BaseModel
from datetime import date

class UserListSchema(BaseModel):
    id:int
    userName:str
    fullName:str
    email:str
    phone:str
    class Config:
        from_attributes=True

class UserCreateSchema(UserListSchema):
    password:str


class AddRegistrationMailLog(BaseModel):
    agent_id:int
    subject:str
    body:str
    mail_sent_to:str
    registration_date:str
