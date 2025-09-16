from pydantic import BaseModel
from typing import Optional

class SearchBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    product_id: Optional[int] = None
    customer_id: Optional[int] = None
    inventory_id: Optional[int] = None
    pricing_id: Optional[int] = None


class SearchCreate(SearchBase):
    pass


class SearchUpdate(SearchBase):
    pass


class SearchOut(SearchBase):
    id: int

    class Config:
        from_attributes = True
