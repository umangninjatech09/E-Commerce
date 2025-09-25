from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.purchase import Purchase
from app.models.product import Product
import requests



router = APIRouter()

ORDER_SERVICE_URL = "http://order_service:8001" 

# 1. Total users
# @router.get("/users/")
# def total_users(db: Session = Depends(get_db)):
#     return {"total_users": db.query(func.count(Customer.id)).scalar() or 0}

@router.get("/users/summary")
def users_summary(
    db: Session = Depends(get_db),
    threshold: int = Query(5, description="Minimum number of orders to consider a user frequent"),
):
    # 1. Total users (from ecommerce DB)
    total_users = db.query(func.count(Customer.id)).scalar() or 0

    # 2. Frequent order-taking users (from the local database)
    frequent_order_users = (
        db.query(Order.customer_id)
        .group_by(Order.customer_id)
        .having(func.count(Order.id) >= threshold)
        .count()
    )

    return {
        "total_users": total_users,
        "frequent_order_users": frequent_order_users,
        "threshold": threshold,
    }

@router.get("/orders/count")
def total_orders():
    response = requests.get(f"{ORDER_SERVICE_URL}/orders")
    return {"total_orders": len(response.json())}

@router.get("/products/count")
def total_products(db: Session = Depends(get_db)):
    return {"total_products": db.query(func.count(Product.id)).scalar() or 0}


@router.get("/suppliers/count")
def total_suppliers(db: Session = Depends(get_db)):
    return {"total_suppliers": db.query(func.count(Supplier.id)).scalar() or 0}

@router.get("/purchases/count")
def total_purchases(db: Session = Depends(get_db)):
    return {"total_purchases": db.query(func.count(Purchase.id)).scalar() or 0}