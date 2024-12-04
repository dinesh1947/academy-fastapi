from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TagListSchema(BaseModel):
    id:int
    tag_name:str
    addedBy:Optional[int]
    created_date:datetime

class CreateTagMailSchema(BaseModel):
    to_tags:str
    avoid_tags:str
    subject:str
    body:str
    mentor_id:int
    manager_id:int
    status:int = 0
    class Config:
        from_attributes=True

class TestingMailSchema(BaseModel):
    subject:str
    body:str
    mentor_id:int
    manager_id:int
    class Config:
        from_attributes=True
    