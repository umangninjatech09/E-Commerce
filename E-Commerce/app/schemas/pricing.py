from pydantic import BaseModel
from app.schemas.product import ProductOut
from typing import Optional, List

class PricingBase(BaseModel):
    currency: str = "USD"
    amount: float
    discount: float = 0.0

class PricingCreate(PricingBase):
    product_id: int

class Pricing(PricingBase):
    id: int
    product: Optional[ProductOut] = None

    class Config:
        from_attributes = True  

class PricingPagination(BaseModel):
    total_records: int
    total_pages: int
    current_page: int
    prev_page: Optional[int]
    next_page: Optional[int]
    limit: int
    items: List[Pricing]