from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from utils.security import get_password_hash, verify_password


def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()

def create_customer(db: Session, customer: CustomerCreate):
    hashed_password = get_password_hash(customer.password)
    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        password_hash=hashed_password
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def authenticate_customer(db: Session, email: str, password: str):
    customer = get_customer_by_email(db, email)
    if not customer:
        return None
    if not verify_password(password, customer.password_hash):
        return None
    return customer



'''
Today's Work Update :
Complete a sma
'''