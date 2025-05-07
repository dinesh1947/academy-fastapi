from typing import List, TypeVar, Generic, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

T = TypeVar('T')

class Paginator(Generic[T]):
    def __init__(self, db: Session, model: T, pydantic_model: BaseModel, page: int = None, page_size: int = None, base_url: str = ""):
        self.page = page if page is not None else 1
        self.page_size = page_size if page_size is not None else 10
        self.db = db
        self.model = model
        self.pydantic_model = pydantic_model
        self.base_url = base_url.rstrip('/')  # Ensure no trailing slash in base URL

    def get_total_count(self) -> int:
        return self.db.query(func.count(self.model.id)).scalar()

    def get_page(self) -> List[T]:
        offset = (self.page - 1) * self.page_size
        results = self.db.query(self.model).offset(offset).limit(self.page_size).all()
        return [self.pydantic_model.from_orm(result) for result in results]

    def get_total_pages(self) -> int:
        total_count = self.get_total_count()
        return total_count // self.page_size + (1 if total_count % self.page_size != 0 else 0)

    def get_page_url(self, page: Optional[int]) -> Optional[str]:
        if page is None or page < 1 or page > self.get_total_pages():
            return None
        return f"{self.base_url}?page={page}&page_size={self.page_size}"

    def get_paginated_response(self) -> dict:
        total_count = self.get_total_count()
        total_pages = self.get_total_pages()

        return {
            "total_count": total_count,
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": total_pages,
            "first": self.get_page_url(1),
            "last": self.get_page_url(total_pages),
            "next": self.get_page_url(self.page + 1) if self.page < total_pages else None,
            "previous": self.get_page_url(self.page - 1) if self.page > 1 else None,
            "results": self.get_page()
        }
