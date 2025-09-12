from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    category: Optional[str] = None
    brand: Optional[str] = None

class ProductCreate(ProductBase):
    pass  

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None

class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 


class ProductWithInventory(BaseModel):
    id: int
    name: str
    description: Optional[str]
    sku: str
    category: Optional[str]
    brand: Optional[str]
    quantity: int   # expects this
    amount
    created_at: datetime


    class Config:
        from_attributes = True
