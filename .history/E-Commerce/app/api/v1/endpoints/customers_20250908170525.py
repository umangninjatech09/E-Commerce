from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.session import get_db
from schemas.customer import CustomerCreate, CustomerOut, Token
from services.customer_service import create_customer, authenticate_customer
from utils.security import decode_token
from models.customer import Customer
import models
import schemas
from utils.security import hash_password, verify_password, create_access_token




@app.post("/register", response_model=schemas.customer.CustomerOut)
def register_customer(payload: schemas.customer.CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.customer.Customer).filter(
        models.customer.Customer.email == payload.email
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_customer = models.customer.Customer(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@app.post("/login")
def login_customer(payload: schemas.customer.CustomerLogin, db: Session = Depends(get_db)):
    customer = db.query(models.customer.Customer).filter(
        models.customer.Customer.email == payload.email
    ).first()
    if not customer or not verify_password(payload.password, customer.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": customer.email})
    return {"access_token": token, "token_type": "bearer"}

def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Customer:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    customer = db.query(Customer).filter(Customer.id == int(payload["sub"])).first()
    if not customer:
        raise HTTPException(status_code=401, detail="Customer not found")
    return customer

@app.get("/me", response_model=CustomerOut)
def read_current_customer(current_customer: Customer = Depends(get_current_customer)):
    return current_customer
