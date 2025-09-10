from pydantic import BaseModel
from typing import Optional

class SearchIndexIn(BaseModel):
    product_id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    stock_status: str
    rating: Optional[float] = 0.0

class SearchIndexOut(SearchIndexIn):
    id: int

    class Config:
        from_attributes = True