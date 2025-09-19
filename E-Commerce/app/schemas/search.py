from pydantic import BaseModel
from typing import Optional
from app.schemas.product import ProductBase
from app.schemas.customer import CustomerResponse
from app.schemas.inventory import InventoryResponse
from app.schemas.pricing import PricingBase

class SearchBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    
class SearchCreate(SearchBase):
    product_id: Optional[int] = None
    customer_id: Optional[int] = None
    inventory_id: Optional[int] = None
    pricing_id: Optional[int] = None

class SearchUpdate(SearchBase):
    product_id: Optional[int] = None
    customer_id: Optional[int] = None
    inventory_id: Optional[int] = None
    pricing_id: Optional[int] = None

class SearchOut(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    
    product: Optional[ProductBase] = None
    customer: Optional[CustomerResponse] = None
    inventory: Optional[InventoryResponse] = None
    pricing: Optional[PricingBase] = None

    class Config:
        from_attributes = True 