from sqlalchemy.orm import Session
from order_service import models, schemas
from datetime import datetime


def create_order(db: Session, order: schemas.OrderCreate, total_amount: float):
    db_order = models.Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_amount=total_amount,
        status="PENDING",
        created_at=datetime.utcnow(),
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(db: Session):
    return db.query(models.Order).all()

def get_order_by_id(db: Session, order)
