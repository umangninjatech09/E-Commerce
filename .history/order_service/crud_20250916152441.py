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

def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update_order(db: Session, order_id: int, order_data: schemas.OrderUpdate, total_amount: float):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.product_id = order_data.product_id
        db_order.customer_id = order_data.customer_id
        db_order.quantity = order_data.quantity
        db_order.total_amount = total_amount
        db.commit()
        db.refresh(db_order)
        return db_order
    return None

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
        return db_order
    return None