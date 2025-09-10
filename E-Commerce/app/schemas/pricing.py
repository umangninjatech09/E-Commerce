from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Price Schemas 
class PriceCreate(BaseModel):
    product_id: int
    base_price: float

class PriceOut(PriceCreate):
    id: int
    product_id: int
    base_price: float
    created_at: datetime

    class Config:
        from_attributes = True

# Discount Schemas 
class DiscountCreate(BaseModel):
    product_id: int
    discount_percentage: float
    start_date: datetime
    end_date: datetime

class DiscountOut(BaseModel):
    id: int
    product_id: int
    discount_percentage: float
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True