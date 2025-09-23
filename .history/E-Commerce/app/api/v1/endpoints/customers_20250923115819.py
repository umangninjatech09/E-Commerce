from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import SessionLocal
from app.schemas.customer import CustomerCreate, CustomerLogin, CustomerResponse
from app.crud import customer as crud_customer
from app.utils.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
from app.utils.response_builder import error_response
from app.models.customer import Customer
from app.utils.pagination import paginate
from app.schemas.common import Page
from app.db.session import get_db

router = APIRouter()

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

@router.get("/{customer_id}", response_model=CustomerResponse)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer_update: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud_customer.get_customer_by_id(db, customer_id)
    if not db_customer:
        return error_response(404, "CustomerNotFound", f"Customer with id {customer_id} not found.")
    if customer_update.password:
        customer_update.password = get_password_hash(customer_update.password)
    updated_customer = crud_customer.update_customer(db, customer_id, customer_update)
    return updated_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    deleted = crud_customer.delete_customer(db, customer_id)
    if not deleted:
        return error_response(404, "CustomerNotFound", f"Cannot delete: customer with id={customer_id} was not found.")
    return {"detail": "Customer deleted successfully"}    
