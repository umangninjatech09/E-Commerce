from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps import get_db
from app.schemas.customer import CustomerCreate, CustomerLogin, CustomerResponse
from services.customer_service import create_customer, get_customer_by_email
from utils.security import verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=CustomerResponse)
def register(customer: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = create_customer(db, customer)
    if not new_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return new_customer

@router.post("/login")
def login(credentials: CustomerLogin, db: Session = Depends(get_db)):
    db_customer = get_customer_by_email(db, credentials.email)
    if not db_customer or not verify_password(credentials.password, db_customer.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": db_customer.email})
    return {"access_token": token, "token_type": "bearer"}
