from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    success: bool = False
    code: int
    error: str
    message: str

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")  # This allows the items type to be dynamic

class PaginationResponse(GenericModel, Generic[T]):
    total_records: int
    total_pages: int
    current_page: int
    prev_page: Optional[int]
    next_page: Optional[int]
    limit: int
    items: List[T]
