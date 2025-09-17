from pydantic import BaseModel
from typing import Optional, List

class InventoryBase(BaseModel):
    product_id: int
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: int

class InventoryResponse(InventoryBase):
    id: int
    class Config:
        from_attributes = True

class InventoryPagination(BaseModel):
    total_records: int
    total_pages: int
    current_page: int
    prev_page: Optional[int]
    next_page: Optional[int]
    limit: int
    items: List[InventoryResponse]