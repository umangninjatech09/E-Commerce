from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate

def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()

def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    update_data = order.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
        return True
    return False