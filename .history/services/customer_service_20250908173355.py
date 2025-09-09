from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from utils.security import hash_password

def create_customer(db: Session, customer: CustomerCreate):
    db_customer = db.query(Customer).filter(Customer.email == customer.email).first()
    if db_customer:
        return None
    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        password_hash=hash_password(customer.password)
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()
