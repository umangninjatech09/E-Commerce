from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import SessionLocal
import httpx



router = APIRouter(prefix="/orders", tags=["orders"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/", response_model=schemas.OrderResponse)
# def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
#     return crud.create_order(db=db, order=order)

CUSTOMER_SERVICE_URL = "http://localhost:8000/customers"
PRODUCT_SERVICE_URL = "http://localhost:8000/products"

@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Validate customer
    try:
        response = httpx.get(f"{CUSTOMER_SERVICE_URL}/{order.customer_id}")
        if response.status_code != 200:
            return error_response(404, "CustomerNotFound", f"Customer with id={order.customer_id} does not exist.")
    except httpx.RequestError:
        return error_response(503, "CustomerServiceUnavailable", "Cannot reach Customer Service.")

    # Validate product
    try:
        response = httpx.get(f"{PRODUCT_SERVICE_URL}/{order.product_id}")
        if response.status_code != 200:
            return error_response(404, "ProductNotFound", f"Product with id={order.product_id} does not exist.")
    except httpx.RequestError:
        return error_response(503, "ProductServiceUnavailable", "Cannot reach Product Service.")

    # Create order
    db_order = crud_order.create_order(db, order)
    return db_order

@router.get("/", response_model=List[schemas.OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.put("/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud.update_order(db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    success = crud.delete_order(db, order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}
