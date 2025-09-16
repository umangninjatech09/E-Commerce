from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import inventory as schemas
from app.crud import inventory as crud

from app.db.session import get_db
from app.utils.response_builder import error_response

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=List[schemas.InventoryResponse])
def list_inventory(db: Session = Depends(get_db)):
    items = crud.get_all_inventory(db)
    if not items:
        return error_response(404, "Not Found", "No inventory items found")
    return items


@router.post("/", response_model=schemas.InventoryResponse)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_inventory(db, inventory)
    except Exception as e:
        return error_response(400, "Bad Request", str(e))


@router.get("/{product_id}", response_model=schemas.InventoryResponse)
def read_inventory(product_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_inventory(db, product_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_item

@router.put("/inventory/{product_id}", response_model=schemas.InventoryResponse)
def update_inventory(product_id: int, inv_update: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    return crud.update_inventory(db, product_id, inv_update.quantity)
