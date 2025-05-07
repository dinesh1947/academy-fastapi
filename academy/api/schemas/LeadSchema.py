from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssignCounsellingSchema(BaseModel):
    counselling_id:int
    assigned_to:int
    log_user:int

class CancelCounsellingSchema(BaseModel):
    counselling_id:int
    log_user:int
