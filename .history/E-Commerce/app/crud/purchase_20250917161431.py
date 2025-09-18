from sqlalchemy.orm import Session
from app.models.purchase import Purchase
from app.models.inventory import Inventory
from app.schemas.purchase import PurchaseCreate


def create_purchase(db: Session, purchase: PurchaseCreate):
    total_amount = purchase.quantity * purchase.unit_cost

    db_purchase = Purchase(
        supplier_id=purchase.supplier_id,
        product_id=purchase.product_id,
        quantity=purchase.quantity,
        unit_cost=purchase.unit_cost,
        total_amount=total_amount,
        payment_status=purchase.payment_status,
    )
    db.add(db_purchase)

    # ✅ Update inventory automatically
    inventory = db.query(Inventory).filter(Inventory.product_id == purchase.product_id).first()

    if inventory:
        inventory.quantity += purchase.quantity
    else:
        inventory = Inventory(product_id=purchase.product_id, quantity=purchase.quantity)
        db.add(inventory)

    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def get_purchases(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Purchase).offset(skip).limit(limit).all()

def get_all_purchase(db: Session):
    return db.query(Purchase).order_by(Purchase.id).all()


def update_purchase(db: Session, purchase_id: int, purchase: PurchaseCreate):
    db_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not db_purchase:
        return None
    

    inventory = db.query(Inventory).filter(Inventory.product_id == db_purchase.product_id).first()
    if inventory:
        inventory.quantity -= db_purchase.quantity

    
    db_purchase.supplier_id = purchase.supplier_id
    db_purchase.product_id = purchase.product_id
    db_purchase.quantity = purchase.quantity
    db_purchase.unit_cost = purchase.unit_cost
    db_purchase.total_amount = purchase.quantity * purchase.unit_cost
    db_purchase.payment_status = purchase.payment_status


    if inventory:
        inventory.quantity += purchase.quantity
    else:
        inventory = Inventory(product_id=purchase.product_id, quantity=p)