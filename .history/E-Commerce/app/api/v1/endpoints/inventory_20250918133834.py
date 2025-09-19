from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import inventory as schemas
from app.crud import inventory as crud
from app.utils.response_builder import error_response
from fastapi import Query
from app.utils.pagination import paginate
from app.schemas.common import Page
from app.models.inventory import Inventory
from app.db.session import get_db

router = APIRouter( tags=["Inventory"])

router = APIRouter()

@router.get("/", response_model=Page[schemas.InventoryResponse])
def list_inventory(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    query = db.query(Inventory)
    return paginate(query, page, size)


@router.post("/", response_model=schemas.InventoryResponse)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    return crud.create_inventory(db, inventory)

@router.get("/inventory/{product_id}", response_model=schemas.InventoryResponse)
def read_inventory(product_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_inventory(db, product_id)
    if not db_item:
        return error_response(404, "InventoryNotFound", f"Inventory for product_id {product_id} not found.")
    return db_item

@router.put("/{product_id}", response_model=schemas.InventoryResponse)
def update_inventory(product_id: int, inv_update: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    updated_item = crud.update_inventory(db, product_id, inv_update.quantity)
    if not updated_item:
        return error_response(404, "InventoryNotFound", f"Cannot update: inventory record for product_id={product_id} was not found.")
    return updated_item

@router.get("/products/", response_model=InventoryPagination)
def get_inventory_limit(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    total, products = crud.get_inventory_limit(db, skip=(page-1)*limit, limit=limit)
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    # Validate page number
    if page < 1 or page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid page number. Total available pages: {total_pages}"
        )

    # Calculate previous and next page numbers
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    # Return structured pagination response
    return {
        "total_records": total,
        "total_pages": total_pages,
        "current_page": page,
        "prev_page": prev_page,
        "next_page": next_page,
        "limit": limit,
        "items": products
    }