from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.crud import order as crud

router = APIRouter()

@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@router.get("/{order_id}", response_model=OrderOut)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.get("/", response_model=List[OrderOut])
def list_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)

@router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    updated = crud.update_order(db, order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    success = crud.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}
