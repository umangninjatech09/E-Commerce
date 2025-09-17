# schemas.py
from pydantic import BaseModel
from datetime import datetime


class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int


class OrderOut(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
