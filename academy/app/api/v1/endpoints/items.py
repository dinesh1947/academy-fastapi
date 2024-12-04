from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db  # Assuming `get_db` is a dependency for database session

router = APIRouter()

@router.get("/items")
def read_item(db: Session = Depends(get_db)):
    return {"code":0, "message":"Getting some error please try after some time"}
