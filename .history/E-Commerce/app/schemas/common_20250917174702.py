from pydantic import BaseModel
from typing import Optional
from typing import Generic, TypeVar, List, Optional


class ErrorResponse(BaseModel):
    success: bool = False
    code: int
    error: str
    message: str