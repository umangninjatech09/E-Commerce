from pydantic import BaseModel

class PricingBase(BaseModel):
    product_id: int
    currency: str
    amount: float
    discount: float = 0.0

class PricingCreate(PricingBase):
    pass

class Pricing(PricingBase):
    id: int

    class Config:
        from_attributes = True   # Pydantic v2
