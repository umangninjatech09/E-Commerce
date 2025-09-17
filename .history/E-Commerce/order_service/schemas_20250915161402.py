from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import OrderStatus

class CustomerInfo(BaseModel):
    id: int
    name: str
    email: str

class ProductInfo(BaseModel):
    id: int
    name: str
    category: str

class OrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    total_amount: float

class OrderUpdate(BaseModel):
    quantity: Optional[int]
    total_amount: Optional[float]
    status: Optional[OrderStatus]

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime]
    customer: Optional[CustomerInfo] = None
    product: Optional[ProductInfo] = None

    class Config:
        from_attributes = True
