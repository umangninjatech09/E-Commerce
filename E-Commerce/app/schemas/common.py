from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    success: bool = False
    code: int
    error: str
    message: str
