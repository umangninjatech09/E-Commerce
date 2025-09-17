from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from typing import List
from order_service import models, schemas, crud, database


# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Order Service")




# Dependency: DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------
# Helpers to validate external IDs
# ------------------------------
import httpx

CUSTOMER_SERVICE_URL = "http://127.0.0.1:8000/customers"
PRODUCT_SERVICE_URL  = "http://127.0.0.1:8000/products"

async def validate_customer(customer_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CUSTOMER_SERVICE_URL}/{customer_id}")
        if resp.status_code == 200:
            return resp.json()
        return None

async def validate_product(product_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
        if resp.status_code == 200:
            return resp.json()
        return None




# ------------------------------
# Endpoints
# ------------------------------

@app.post("/orders", response_model=schemas.OrderOut)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Validate customer
    customer = await validate_customer(order.customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Invalid customer ID")

    # Validate product
    product = await validate_product(order.product_id)
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    # Save order in DB
    return crud.create_order(db, order)


@app.get("/orders", response_model=List[schemas.OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)


@app.get("/customers-orders")
async def get_customers_with_orders(db: Session = Depends(get_db)):
    """Fetch all customers with their orders"""
    result = []

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CUSTOMER_SERVICE_URL}/customers")
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to fetch customers")
            customers = response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling customer_service: {str(e)}")

    for cust in customers:
        orders = db.query(models.Order).filter(models.Order.customer_id == cust["id"]).all()
        result.append({
            "id": cust["id"],
            "name": cust["name"],
            "email": cust["email"],
            "orders": [
                {
                    "order_id": o.id,
                    "product_id": o.product_id,
                    "quantity": o.quantity,
                    "total_amount": o.total_amount,
                    "status": o.status
                }
                for o in orders
            ]
        })

    return result
