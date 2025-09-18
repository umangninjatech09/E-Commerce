from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.purchase.Purchase)
def create_purchase(purchase: schemas.purchase.PurchaseCreate, db: Session = Depends(get_db)):
    return crud.purchase.create_purchase(db, purchase)


@router.get("/", response_model=list[schemas.purchase.Purchase])
def read_purchases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.purchase.get_purchases(db, skip, limit)
