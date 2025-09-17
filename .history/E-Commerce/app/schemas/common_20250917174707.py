from pydantic import BaseModel
from typing import Optional
from typing import Generic, TypeVar, List, Optional
from pydantic.generics import GenericModel

class ErrorResponse(BaseModel):
    success: bool = False
    code: int
    error: str
    message: str