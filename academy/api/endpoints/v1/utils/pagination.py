from typing import List, TypeVar, Generic, Optional,Type
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session,Query
from sqlalchemy import func
from pydantic import BaseModel
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

load_dotenv()


from typing import Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel




BASE_URL = os.getenv("BASE_URL")



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






def paginate_query(
    *,
    request: Request,
    query: Query,
    schema: Type[T],
    page: int,
    page_size: int
) -> PaginatedResponse[T]:
    offset = (page - 1) * page_size
    total_count = query.order_by(None).count()  

    results = query.offset(offset).limit(page_size).all()
    base_url = BASE_URL
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













def build_pagination_urls(request: Request, page: int, page_count: int) -> dict:
    base_url = str(request.url).split('?')[0]
    query_params = dict(request.query_params)

    def build_url(page_num: int):
        params = query_params.copy()
        params['page'] = page_num
        return f"{base_url}?{urlencode(params)}"

    return {
        "next": build_url(page + 1) if page < page_count else None,
        "previous": build_url(page - 1) if page > 1 else None,
        "first_page": build_url(1) if page_count > 0 else None,
        "last_page": build_url(page_count) if page_count > 0 else None,
    }