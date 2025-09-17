from fastapi import HTTPException
from typing import List, TypeVar
from app.schemas.common import PaginationResponse

T = TypeVar("T")

def paginate(items: List[T], total: int, page: int, limit: int) -> PaginationResponse[T]:
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    if page < 1 or page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid page number. Total available pages: {total_pages}"
        )

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return PaginationResponse[T](
        total_records=total,
        total_pages=total_pages,
        current_page=page,
        prev_page=prev_page,
        next_page=next_page,
        limit=limit,
        items=items
    )
