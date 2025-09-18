from sqlalchemy.orm import Session
from app.schemas import purchase as schemas


def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    total_amount = purchase.quantity * purchase.unit_cost

    db_purchase = models.Purchase(
        supplier_id=purchase.supplier_id,
        product_id=purchase.product_id,
        quantity=purchase.quantity,
        unit_cost=purchase.unit_cost,
        total_amount=total_amount,
        payment_status=purchase.payment_status,
    )
    db.add(db_purchase)

    inventory = db.query(models.Inventory).filter(models.Inventory.product_id == purchase.product_id).first()
    if inventory:
        inventory.quantity += purchase.quantity
    else:
        new_inventory = models.Inventory(
            product_id=purchase.product_id,
            quantity=purchase.quantity
        )
        db.add(new_inventory)
    
    db.commit()
    db.refresh(db_purchase)
    return db_purchase
