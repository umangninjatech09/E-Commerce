from sqlalchemy.orm import Session
from app.models import inventory as models

def create_inventory(db: Session, inventory: schemas.InventoryCreate):
    db_item = models.Inventory(**inventory.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_inventory(db: Session, product_id: int):
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()

def update_inventory(db: Session, product_id: int, qty: int):
    item = get_inventory(db, product_id)
    if item:
        item.quantity = qty
        db.commit()
        db.refresh(item)
    return item
