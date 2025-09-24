from sqlalchemy.orm import Session
from app.models import inventory as models
from app.schemas import inventory as schemas
from app.crud import inventory as crud_inventory

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

def get_all_inventory(db: Session):
    return db.query(models.Inventory).all()

def get_inventory_limit(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(models.Inventory)
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    return total, products
    
def delete_inventory(db: Session, product_id: int):
    item = get_inventory(db, product_id)
    if item:
        db.delete(item)
        db.commit()
        return True
    return False