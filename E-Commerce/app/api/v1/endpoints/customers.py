from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import SessionLocal
from app.schemas.customer import CustomerCreate, CustomerLogin, CustomerResponse
from app.crud import customer as crud_customer
from app.utils.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
from app.utils.response_builder import error_response
from app.schemas.customer import CustomerPagination


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

@router.get("/customer/", response_model=CustomerPagination)
def get_customer_limit(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    total, products = crud_customer.get_customer_limit(db, skip=(page-1)*limit, limit=limit)
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    # Validate page number
    if page < 1 or page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid page number. Total available pages: {total_pages}"
        )

    # Calculate previous and next page numbers
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    # Return structured pagination response
    return {
        "total_records": total,
        "total_pages": total_pages,
        "current_page": page,
        "prev_page": prev_page,
        "next_page": next_page,
        "limit": limit,
        "items": products
    }