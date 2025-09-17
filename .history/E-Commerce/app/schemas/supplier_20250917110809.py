from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class SupplierBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    status: Literal["active", "inactive"] = "active"


class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: Optional[Literal["active", "inactive"]] = None

class Su