from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from academy.app.config.database import get_sync_db  # Assuming `get_db` is a dependency for database session

router = APIRouter()

@router.get("/items")
def read_item(db: Session = Depends(get_sync_db)):
    return {"code":0, "message":"Getting some error please try after some time"}
