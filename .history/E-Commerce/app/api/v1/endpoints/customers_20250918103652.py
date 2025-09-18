from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import SessionLocal
from app.schemas.customer import CustomerCreate, CustomerLogin, CustomerResponse
from app.crud import customer as crud_customer
from app.utils.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
from app.db.session import get_db
from typing import List
from app.utils.response_builder import error_response
from app.models.customer import Customer
from fastapi import Query


router = APIRouter()


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_customer.get_customer(db, customer_id=customer_id)
    if not db_customer:
        return error_response(404, "Not Found", "Customer not found")
    return db_customer


@router.post("/register", response_model=CustomerResponse)
def register(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud_customer.get_customer_by_email(db, email=customer.email)
    if db_customer:
        return error_response(400, "DuplicateEmail", "This email address is already registered.")
    return crud_customer.create_customer(db, customer)

@router.post("/login")
def login(customer: CustomerLogin, db: Session = Depends(get_db)):
    db_customer = crud_customer.authenticate_customer(db, customer.email, customer.password)
    if not db_customer:
         return error_response(401, "Invalid credentials", "The email or password provided is incorrect.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_customer.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=Page[CustomerResponse])
def list_customers(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    query = db.query(Customer)
    return paginate(query, page, size)    

