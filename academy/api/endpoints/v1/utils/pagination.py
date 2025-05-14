from typing import List, TypeVar, Generic, Optional
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session,Query
from sqlalchemy import func
from pydantic import BaseModel







from typing import Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel

T = TypeVar('T')

class PaginatedResponse(GenericModel, Generic[T]):
    total_count: int
    page: int
    page_size: int
    total_pages: int
    first: Optional[str] = None
    last: Optional[str] = None
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[T]



from typing import Type, Generic
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

class Paginator(Generic[T]):
    def __init__(
        self,
        *,
        db: Session,
        model,
        pydantic_model: Type[BaseModel],
        page: int = 1,
        page_size: int = 10,
        base_url: str = ""
    ):
        self.db = db
        self.model = model
        self.schema = pydantic_model
        self.page = page
        self.page_size = page_size
        self.base_url = base_url.rstrip('/')

    def get_total_count(self) -> int:
        return self.db.query(func.count(self.model.id)).scalar()

    def get_items(self) -> List[T]:
        offset = (self.page - 1) * self.page_size
        results = self.db.query(self.model).offset(offset).limit(self.page_size).all()
        return [self.schema.from_orm(obj) for obj in results]

    def get_total_pages(self) -> int:
        total_count = self.get_total_count()
        return (total_count + self.page_size - 1) // self.page_size

    def get_url(self, page: int) -> Optional[str]:
        if page < 1 or page > self.get_total_pages():
            return None
        return f"{self.base_url}?page={page}&page_size={self.page_size}"

    def get_response(self) -> PaginatedResponse[T]:
        total_count = self.get_total_count()
        total_pages = self.get_total_pages()
        return PaginatedResponse[T](
            total_count=total_count,
            page=self.page,
            page_size=self.page_size,
            total_pages=total_pages,
            first=self.get_url(1),
            last=self.get_url(total_pages),
            next=self.get_url(self.page + 1) if self.page < total_pages else None,
            previous=self.get_url(self.page - 1) if self.page > 1 else None,
            results=self.get_items()
        )









def paginate_query(
    *,
    request: Request,
    query: Query,
    schema: Type[T],
    page: int,
    page_size: int
) -> PaginatedResponse[T]:
    offset = (page - 1) * page_size
    total_count = query.order_by(None).count()  # `order_by(None)` avoids unnecessary ORDER BY in count

    results = query.offset(offset).limit(page_size).all()
    base_url = str(request.url).split('?')[0]
    total_pages = (total_count + page_size - 1) // page_size

    return PaginatedResponse[T](
        total_count=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        first=f"{base_url}?page=1&page_size={page_size}",
        last=f"{base_url}?page={total_pages}&page_size={page_size}",
        next=f"{base_url}?page={page + 1}&page_size={page_size}" if page < total_pages else None,
        previous=f"{base_url}?page={page - 1}&page_size={page_size}" if page > 1 else None,
        results=[schema.from_orm(obj) for obj in results]
    )