from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.utils.security import ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, verify_password
from app.crud import customer as crud_customer

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

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_all_customers(db: Session):
    return db.query(Customer).order_by(Customer.id).all()

def get_customer_limit(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(Customer)
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    return total, products

def get