from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.models.supplier import Supplier
from app.models.purchase import Purchase

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# 1. Total users
@router.get("/users/count")
def total_users(db: Session = Depends(get_db)):
    return {"total_users": db.query(func.count(Customer.id)).scalar() or 0}
