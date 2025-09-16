from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    quantity: Optional[int]
    total_amount: Optional[float]
    status: Optional[str]

class OrderOut(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
