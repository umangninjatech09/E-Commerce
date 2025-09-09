from pydantic import BaseModel, EmailStr

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    
class CustomerCreate(CustomerBase):
    password: str

class CustomerLogin(BaseModel):
    email: EmailStr
    password: str

class CustomerOut(CustomerBase):
    id: int

    class Config:
        orm_mode = True