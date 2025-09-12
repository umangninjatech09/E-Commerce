from pydantic import BaseModel
from app.schemas.product import ProductOut
from typing import Optional

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
