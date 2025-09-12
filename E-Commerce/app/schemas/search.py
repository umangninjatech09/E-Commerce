from pydantic import BaseModel
from typing import Optional


class SearchIndexBase(BaseModel):
    product_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    entity_type: str
    entity_id: int


class SearchIndexCreate(SearchIndexBase):
    pass


class SearchIndexUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None


class SearchIndexOut(SearchIndexBase):
    id: int

    class Config:
        from_attributes = True