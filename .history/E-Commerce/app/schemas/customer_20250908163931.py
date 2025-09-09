from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class CustomerLogin(BaseModel):
    email: EmailStr
    password: str

class CustomerOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

    
class CustomerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"