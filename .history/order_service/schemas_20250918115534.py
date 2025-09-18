# schemas.py
from pydantic import BaseModel
from datetime import datetime


class OrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderOut(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    amount: float
    discount: float
    total_amount: float
    status: Delivered
    created_at: datetime

    class Config:
        from_attributes = True

