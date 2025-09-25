from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.customer import Customer
from .models.order import Order


router = APIRouter()


# 1. Total users
# Users Dashboard
@router.get("/users/summary")
def users_summary(
    db: Session = Depends(get_db),
    threshold: int = Query(5, description="Minimum number of orders to consider a user frequent"),
):
    # 1. Total users
    total_users = db.query(func.count(Customer.id)).scalar() or 0

    # 2. Frequent order-taking users
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

