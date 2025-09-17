from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str

# Product schema
class ProductResponse(BaseModel):
    id: int
    name: str
    category: str

class OrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: Optional[str] = "pending"

class OrderUpdate(BaseModel):
    quantity: Optional[int]
    total_amount: Optional[float]
    status: Optional[str]

class OrderResponse(OrderBase):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    customer: CustomerResponse  
    product: ProductResponse    

    class Config:
        from_attributes = True
