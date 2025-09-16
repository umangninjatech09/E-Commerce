import httpx
from sqlalchemy.orm import Session
from . import models, schemas


CUSTOMER_SERVICE_URL = "http://localhost:8000/customers"
PRODUCT_SERVICE_URL = "http://localhost:8000/products"

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return None

    # fetch customer info
    try:
        r = httpx.get(f"{CUSTOMER_SERVICE_URL}/{db_order.customer_id}")
        db_order.customer = r.json() if r.status_code == 200 else None
    except:
        db_order.customer = None

    # fetch product info
    try:
        r = httpx.get(f"{PRODUCT_SERVICE_URL}/{db_order.product_id}")
        db_order.product = r.json() if r.status_code == 200 else None
    except:
        db_order.product = None

    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return [get_order(db, o.id) for o in orders]

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        for key, value in order.dict(exclude_unset=True).items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order