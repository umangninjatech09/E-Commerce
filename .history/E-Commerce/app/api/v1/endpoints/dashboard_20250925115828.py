from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.customer import Customer


router = APIRouter()


# 1. Total users
@router.get("/users/")
def total_users(db: Session = Depends(get_db)):
    return {"total_users": db.query(func.count(Customer.id)).scalar() or 0}

@router.get("/suppliers/count")
def total_suppliers(db: Session = Depends(get_db)):
    return {"total_suppliers": db.query(func.count(Supplier.id)).scalar() or 0}