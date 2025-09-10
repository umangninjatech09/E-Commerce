from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate

def create_order(db: Session, order_data: OrderCreate, validated_items: list, total_amount: float):
    order = Order(user_id=order_data.user_id, total_amount=total_amount, status="PLACED")
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in validated_items:
        db_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            qty=item["qty"],
            price_snapshot=item["price"]
        )
        db.add(db_item)

    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def cancel_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = "CANCELLED"
        db.commit()
        db.refresh(order)
    return order