from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.purchase import Purchase
import requests



router = APIRouter()

ORDER_SERVICE_URL = "http://order-service:8000" 

# 1. Total users
@router.get("/users/")
def total_users(db: Session = Depends(get_db)):
    return {"total_users": db.query(func.count(Customer.id)).scalar() or 0}

@router.get("/orders/count")
def total_orders():
    response = requests.get(f"{ORDER_SERVICE_URL}/orders")
    return response.json()


@router.get("/suppliers/count")
def total_suppliers(db: Session = Depends(get_db)):
    return {"total_suppliers": db.query(func.count(Supplier.id)).scalar() or 0}

@router.get("/purchases/count")
def total_purchases(db: Session = Depends(get_db)):
    return {"total_purchases": db.query(func.count(Purchase.id)).scalar() or 0}