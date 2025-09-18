from sqlalchemy.orm import Session
from app import models, schemas

def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    total_amount = purchase.quantity * purchase.unit_cost

    