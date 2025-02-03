from typing import List, TypeVar, Generic
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel  # Add this import

T = TypeVar('T')  # Define a generic type for model



class Paginator(Generic[T]):
    def __init__(self, db: Session, model: T, pydantic_model: BaseModel, page: int = None, page_size: int = None):
        # Use default values if not provided
        self.page = page if page is not None else 1
        self.page_size = page_size if page_size is not None else 10
        self.db = db
        self.model = model
        self.pydantic_model = pydantic_model  # Accept the Pydantic model for conversion

    def get_total_count(self) -> int:
        return self.db.query(func.count(self.model.id)).scalar()

    def get_page(self) -> List[T]:
        print("fffffffffffffffffffffffffffffffffff")
        offset = (self.page - 1) * self.page_size
        print("fffffffffffffffffffffffffffffffffff>>>>>>>>>>>>")
        print("self.model", self.model)
        print("offset", offset)
        print("page_size", self.page_size)

        results = self.db.query(self.model).offset(offset).limit(self.page_size).all()

        print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLUUUUUUUUUUUUUUUUUUUUUUUUU")
        print("self.pydantic_model",self.pydantic_model)

        # Convert SQLAlchemy models to Pydantic models
        return [self.pydantic_model.from_orm(result) for result in results]

    def get_first_page(self) -> List[T]:
        self.page = 1
        return self.get_page()

    def get_last_page(self) -> List[T]:
        total_count = self.get_total_count()
        last_page = total_count // self.page_size + (1 if total_count % self.page_size != 0 else 0)
        self.page = last_page
        return self.get_page()

    def get_next_page(self) -> List[T]:
        if self.page * self.page_size >= self.get_total_count():
            raise HTTPException(status_code=404, detail="No more pages")
        self.page += 1
        return self.get_page()

    def get_previous_page(self) -> List[T]:
        if self.page <= 1:
            raise HTTPException(status_code=404, detail="No previous pages")
        self.page -= 1
        return self.get_page()

    def get_paginated_response(self) -> dict:
        total_count = self.get_total_count()
        print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDdddd")
        results = self.get_page()
        print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDddddtttttttttttttttttt")
        print(f"Results fetched: {results}")  # Check what is returned
        return {
            "total_count": total_count,
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": total_count // self.page_size + (1 if total_count % self.page_size != 0 else 0),
            "results": results
        }
    

