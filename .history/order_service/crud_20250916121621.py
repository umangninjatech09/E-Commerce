from sqlalchemy.orm import Session
from order_service import models, schemas

def create_order(db: Session, order: schemas.OrderCreate):


def get_orders(db: Session):
    return db.query(models.Order).all()
