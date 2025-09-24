from pydantic import BaseModel
from typing import Optional
 
class SearchIndexBase(BaseModel):
    product_id: Optional[int] = None
    customer_id: Optional[int] = None
    inventory_id: Optional[int] = None
    pricing_id: Optional[int] = None
 
class SearchIndexCreate(SearchIndexBase):
    pass
 
class SearchIndexOut(SearchIndexBase):
    id: int
    product_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
 
    class Config:
        from_attributes = True
 
 