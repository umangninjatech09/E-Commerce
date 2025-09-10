from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItemIn(BaseModel):
    product_id: int
    qty: int

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemIn]

class OrderItemOut(BaseModel):
    product_id: int
    qty: int
    price_snapshot: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True