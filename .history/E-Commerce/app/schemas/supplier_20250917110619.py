from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class SupplierBase(BaseModel):
    name: str
    contact_email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    status: Literal['active', 'inactive'] = 'active'