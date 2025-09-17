from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class SupplierBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    status: Literal["active", "inactive"] = "active"