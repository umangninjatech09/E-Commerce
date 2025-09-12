from pydantic import BaseModel
from typing import Optional



class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None


class ProductCreate(ProductBase):
    pass  # Inherits all fields from ProductBase for creation


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True  
