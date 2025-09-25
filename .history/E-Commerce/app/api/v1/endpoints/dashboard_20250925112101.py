from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.customer import Customer


router = APIRouter(
# 1. Total users
@router.get("/users/count")
def total_users(db: Session = Depends(get_db)):
    return {"total_users": db.query(func.count(Customer.id)).scalar() or 0}
