from pydantic import BaseModel
from typing import Optional
from typing import Generic, TypeVar, List, Optional

class ErrorResponse(BaseModel):
    success: bool = False
    code: int
    error: str
    message: str

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    pages: int
    next_page: Optional[int]
    prev_page: Optional[int]
    items: List[T]