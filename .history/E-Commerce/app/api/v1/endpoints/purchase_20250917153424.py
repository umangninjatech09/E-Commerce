from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.purchase import Purchase, PurchaseCreate
from app.crud.purchase  
from app.db.session import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=Purchase)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    return create_purchase(db, purchase)


@router.get("/", response_model=List[Purchase])
def read_purchases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_purchases(db, skip, limit)

@router.get("/", response_model=List[Purchase])
def list_purchase(db: Session = Depends(get_db)):
    return get_all_purchase(db)