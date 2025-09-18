from sqlalchemy.orm import Session
from app import models, schemas

def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    total_amount = purchase.quantity * purchase.unit_cost

    db_purchase = models.Purchase(
        supplier_id=purchase.supplier_id,
        product_id=purchase.product_id,
        quantity=purchase.quantity,
        unit_cost=purchase.unit_cost,
        total_amount=total_amount,
        payment_status="pending",
    )