from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.purchase import Purchase, PurchaseCreate
from app.crud.purchase import create_purchase, get_all_purchase, get_purchases, update_purchase, delete_purchase
from app.db.session import get_db
from typing import List
from fastapi import Query
from app.utils.pagination import paginate
from app.schemas.common import Page
from app.schemas.purchase import Purchase
from app.models.purchase import Purchase as PurchaseModel
from app.crud.purchase import create_purchase as crud_create_purchase
from app.utils.response_builder import error_response


router = APIRouter()

@router.post("/", response_model=Purchase)
def api_create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    return crud_create_purchase(db, purchase)

@router.get("/", response_model=Page[Purchase])
def list_purchase(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    query = db.query(PurchaseModel)  
    return paginate(query, page, size)


@router.put("/{purchase_id}", response_model=Purchase)
def update_purchases(purchase_id: int, purchase: PurchaseCreate, db: Session = Depends(get_db)):
    db_purchase = update_purchase(db, purchase_id, purchase)
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase

@router.delete("/{purchase_id}", response_model=Purchase)
def delete_purchases(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = delete_purchase(db, purchase_id)
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase