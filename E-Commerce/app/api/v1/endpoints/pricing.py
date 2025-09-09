from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas import pricing as schemas
from app.crud import pricing as crud

router = APIRouter()

# Price Endpoints 

@router.post("/pricing/set", response_model=schemas.PriceOut)
def set_price(data: schemas.PriceCreate, db: Session = Depends(get_db)):
    return crud.create_or_update_price(db, data)

@router.get("/pricing/{product_id}", response_model=schemas.PriceOut)
def get_price(product_id: str, db: Session = Depends(get_db)):
    price = crud.get_price_by_product(db, product_id)
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    return price

@router.get("/pricing/", response_model=List[schemas.PriceOut])
def list_prices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_prices(db, skip=skip, limit=limit)

@router.delete("/pricing/{product_id}")
def delete_price(product_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_price(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Price not found")
    return {"detail": "Price deleted successfully"}

# Discount Endpoints 

@router.post("/discount/set", response_model=schemas.DiscountOut)
def set_discount(data: schemas.DiscountCreate, db: Session = Depends(get_db)):
    return crud.create_or_update_discount(db, data)

@router.get("/discount/{product_id}", response_model=List[schemas.DiscountOut])
def get_discounts(product_id: str, db: Session = Depends(get_db)):
    discounts = crud.get_discounts_by_product(db, product_id)
    if not discounts:
        raise HTTPException(status_code=404, detail="No discounts found")
    return discounts

@router.delete("/discount/{discount_id}")
def delete_discount(discount_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_discount(db, discount_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Discount not found")
    return {"detail": "Discount deleted successfully"}