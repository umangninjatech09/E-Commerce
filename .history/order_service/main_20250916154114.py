import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from order_service import models, schemas, crud, database
from typing import List

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Order Service")

# External services
CUSTOMER_SERVICE_URL = "http://127.0.0.1:8000"
PRODUCT_SERVICE_URL = "http://127.0.0.1:8000/products/products"
PRICING_SERVICE_URL = "http://127.0.0.1:8000/pricing/pricing"
INVENTORY_SERVICE_URL = "http://127.0.0.1:8000/inventory/inventory"



# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helpers (sync httpx)

async def validate_customer(customer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}")
        if response.status_code == 200:
            return response.json()
    return None

async def validate_product(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
        if response.status_code == 200:
            return response.json()
    return None

async def validate_pricing(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRICING_SERVICE_URL}/{product_id}")
        if response.status_code == 200:
            return response.json()
    return None

async def update_inventory(product_id: int, quantity: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{INVENTORY_SERVICE_URL}/{product_id}")
            if response.status_code != 200:
                return None
            
            inventory = response.json()
            current_stock = inventory["quantity"]

            if current_stock < quantity:
                return None
            
            new_quantity = current_stock - quantity
            update_payload = {"quantity": new_quantity}

            put_response = await client.put(
                f"{INVENTORY_SERVICE_URL}/{product_id}", json=update_payload
            )
            if put_response.status_code == 200:
                return put_response.json()
        
        except Exception as e:
            print(f"Error updating inventory: {str(e)}")
    return None

# Endpoints

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

    # ✅ Validate pricing
    pricing = await validate_pricing(order.product_id)
    if not pricing:
        raise HTTPException(status_code=400, detail="Pricing not found for product")

    price = pricing["amount"]
    discount = pricing.get("discount", 0)

    discounted_price = price * (1 - discount / 100)
    total_amount = round(order.quantity * discounted_price, 2)

    inventory = await update_inventory(order.product_id, order.quantity)
    if not inventory:
        raise HTTPException(status_code=400, detail="Insufficient inventory or product not found")

    # Save order
    return crud.create_order(db, order, total_amount)


@app.get("/orders", response_model=List[schemas.OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.put("/orders/{order_id}", response_model=schemas.OrderOut)
async def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    existing_order = crud.get_order_by_id(db, order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.product_id != existing_order.product_id:
        product = await validate_product(order.product_id)
        if not product:
            raise HTTPException(status_code=400, detail="Invalid customer ")