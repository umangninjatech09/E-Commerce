from sqlalchemy.orm import Session
from db.session import get_db
from models.customer import Customer
from utils.security import hash_password, verify_password, create_access_token

def create_customer(db: Session, name: str, email: str, password: str):
    existing = db.query(Customer).filter(Customer.email == email).first()
    if existing:
        raise ValueError("Email already registered")
    customer = Customer(
        name=name,
        email=email,
        password_hash=hash_password(password)
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def authenticate_customer(db: Session, email: str, password: str):
    customer = db.query(Customer).filter(Customer.email == email).first()
    if not customer or not verify_password(password, customer.password_hash):
        return None
    token = create_access_token({"sub": str(customer.id)})
    return token, customer