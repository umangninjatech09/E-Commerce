from pydantic import BaseModel, EmailStr
from typing import List, Optional

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class CustomerLogin(BaseModel):
    email: EmailStr
    password: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class CustomerPagination(BaseModel):
    total_records: int
    total_pages: int
    current_page: int
    prev_page: Optional[int]
    next_page: Optional[int]
    limit: int
    items: List[CustomerResponse]