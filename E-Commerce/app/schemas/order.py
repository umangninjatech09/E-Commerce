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

class OrderUpdate(BaseModel):
    quantity: int | None = None
    total_amount: float | None = None
    status: str | None = None

class OrderOut(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
