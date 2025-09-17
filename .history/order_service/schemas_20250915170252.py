from pydantic import BaseModel
from datetime import datetime


class OrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: str = "pending"


class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
