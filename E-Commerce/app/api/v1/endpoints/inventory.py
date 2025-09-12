from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import inventory as schemas
from app.crud import inventory as crud

from app.db.session import get_db

router = APIRouter()

@router.post("/inventory/", response_model=schemas.InventoryResponse)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    return crud.create_inventory(db, inventory)

@router.get("/inventory/{product_id}", response_model=schemas.InventoryResponse)
def read_inventory(product_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_inventory(db, product_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_item

@router.put("/inventory/{product_id}", response_model=schemas.InventoryResponse)
def update_inventory(product_id: int, inv_update: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    return crud.update_inventory(db, product_id, inv_update.quantity)
