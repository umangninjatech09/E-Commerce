from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.purchase import Purchase, PurchaseCreate
from app.crud.purchase import create_purchase, get_all_purchase, get_purchases, update_purchase, delete_purchase
from app.db.session import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=Purchase)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    return create_purchase(db, purchase)


@router.get("/", response_model=List[Purchase])
def list_purchase(db: Session = Depends(get_db)):
    return get_all_purchase(db)


@router.put("/{purchase_id}", response_model=Purchase)
def update_purchase(purchase_id: int, purchase: PurchaseCreate, db: Session = Depends(get_db)):
    db_purchase = update_purchase(db, purchase_id, purchase)
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase

@router.delete("/{purchase_id}", response_model=Purchase)
