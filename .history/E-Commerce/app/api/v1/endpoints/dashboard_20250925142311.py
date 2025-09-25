from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.purchase import Purchase
from app.models.product import Product
import requests
import httpx
from fastapi import HTTPException


router = APIRouter()

ORDER_SERVICE_URL = "http://order_service:8001" 
ORDER_SERVICE 

@router.get("/users/")
async def users_summary(
    db: Session = Depends(get_db),
    threshold: int = Query(5, description="Minimum number of orders to consider a user frequent"),
):
    # 1. Total users (from ecommerce DB)
    total_users = db.query(func.count(Customer.id)).scalar() or 0

    # 2. Fetch the frequent order-taking users from the Order Microservice
    async with httpx.AsyncClient() as client:
        response = await client.get(
            ORDER_SERVICE_URL,
            params={"threshold": threshold}  # Pass the threshold to the order service
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching order data from the order service")
        
        frequent_order_users = response.json().get("frequent_order_users", 0)

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