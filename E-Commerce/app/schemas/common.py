from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel

class ErrorResponse(BaseModel):
    success: bool = False
    code: int
    error: str
    message: str

# Pagination
T = TypeVar("T")

class PaginationResponse(GenericModel, Generic[T]):
    total_records: int
    total_pages: int
    current_page: int
    prev_page: Optional[int]
    next_page: Optional[int]
    limit: int
    items: List[T]
