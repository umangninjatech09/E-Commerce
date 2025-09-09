from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import SessionLocal
from utils.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.customer import CustomerCreate, CustomerLogin, CustomerResponse
from app.crud import customer as crud_customer



router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=CustomerResponse)
def register(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud_customer.get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_customer.create_customer(db, customer)

@router.post("/login")
def login(customer: CustomerLogin, db: Session = Depends(get_db)):
    db_customer = crud_customer.authenticate_customer(db, customer.email, customer.password)
    if not db_customer:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_customer.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
