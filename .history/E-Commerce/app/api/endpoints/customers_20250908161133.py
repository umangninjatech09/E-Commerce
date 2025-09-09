from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.session import get_db
from schemas.customer import CustomerCreate, CustomerOut, Token
from services.customer_service import create_customer, authenticate_customer
from utils.security import decode_token
from models.customer import Customer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/register", response_model=CustomerOut)
def register(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        new_customer = create_customer(db, customer.name, customer.email, customer.password)
        return new_customer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token, customer = authenticate_customer(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Customer:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    customer = db.query(Customer).filter(Customer.id == int(payload["sub"])).first()
    if not customer:
        raise HTTPException(status_code=401, detail="Customer not found")
    return customer

@router.get("/me", response_model=CustomerOut)
def read_current_customer(current_customer: Customer = Depends(get_current_customer)):
    return current_customer
