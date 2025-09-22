import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from order_service import models, schemas, crud, database
from typing import List
from utils.middleware import jwt_middleware


# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Order Service")

# JWT Middleware (assuming you have implemented it)
# from app.middleware.jwt import jwt_middleware

app.middleware("http")(jwt_middleware)

# External services
CUSTOMER_SERVICE_URL = "http://127.0.0.1:8000"
PRODUCT_SERVICE_URL = "http://127.0.0.1:8000/products"
PRICING_SERVICE_URL = "http://127.0.0.1:8000/pricing"
INVENTORY_SERVICE_URL = "http://127.0.0.1:8000/inventory"



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

async def update_inventory(product_id: int, quantity_change: int):
    """
    Adjust inventory: Positive -> add, Negative -> subtract.
    Returns updated inventory JSON if successful.
    """
    async with httpx.AsyncClient() as client:
        # 1️⃣ Get current stock
        response = await client.get(f"{INVENTORY_SERVICE_URL}/{product_id}")
        if response.status_code != 200:
            return None
        inventory = response.json()
        current_stock = inventory.get("quantity", 0)

        # 2️⃣ Check stock
        new_quantity = current_stock + quantity_change
        if new_quantity < 0:
            return None  # Insufficient stock

        # 3️⃣ Update inventory
        put_response = await client.put(
            f"{INVENTORY_SERVICE_URL}/{product_id}",
            json={"quantity": new_quantity}
        )
        if put_response.status_code == 200:
            return put_response.json()
    return None

# Endpoints

@app.post("/orders", response_model=schemas.OrderOut)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Validate customer
    customer = await validate_customer(order.customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="InvalidCustomer: Customer not found")

    # Validate product
    product = await validate_product(order.product_id)
    if not product:
        raise HTTPException(status_code=400, detail="InvalidProduct: Product not found")

    # Validate pricing
    pricing = await validate_pricing(order.product_id)
    if not pricing:
        raise HTTPException(status_code=400, detail="PricingNotFound: No pricing found for this product")
    
    price = pricing["amount"]
    discount = pricing.get("discount", 0)
    discounted_price = price * (1 - discount / 100)
    total_amount = round(order.quantity * discounted_price, 2)

    # Update inventory
    inventory_update = await update_inventory(order.product_id, -order.quantity)
    if not inventory_update:
        raise HTTPException(status_code=400, detail="InventoryError: Insufficient inventory")

    # Create order in DB
    new_order = models.Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_amount=total_amount,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return schemas.OrderOut(
        id=new_order.id,
        customer_id=new_order.customer_id,
        product_id=new_order.product_id,
        quantity=new_order.quantity,
        amount=price,
        discount=discount,
        total_amount=total_amount,
        status=new_order.status,
        created_at=new_order.created_at
    )



# @app.get("/orders", response_model=List[schemas.OrderOut])
# def list_orders(db: Session = Depends(get_db)):
#     return crud.get_orders(db)

@app.get("/orders", response_model=List[schemas.OrderOut])
async def list_orders(db: Session = Depends(get_db)):
    orders = crud.get_orders(db)
    orders_with_details = []

    for order in orders:
        pricing = await validate_pricing(order.product_id)
        if not pricing:
            raise HTTPException(status_code=400, detail=f"Pricing not found for product {order.product_id}")
        price = pricing["amount"]
        discount = pricing.get("discount", 0)
        total_amount = round(order.quantity * price * (1 - discount / 100), 2)
        orders_with_details.append(schemas.OrderOut(
            id=order.id,
            customer_id=order.customer_id,
            product_id=order.product_id,
            quantity=order.quantity,
            amount=price,
            discount=discount,
            total_amount=total_amount,
            status=order.status,
            created_at=order.created_at
        ))
    return orders_with_details



@app.put("/orders/{order_id}", response_model=schemas.OrderOut)
async def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    existing_order = crud.get_order_by_id(db, order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Validate changes
    if order.customer_id != existing_order.customer_id:
        customer = await validate_customer(order.customer_id)
        if not customer:
            raise HTTPException(status_code=400, detail="InvalidCustomer: Customer not found")
    if order.product_id != existing_order.product_id:
        product = await validate_product(order.product_id)
        if not product:
            raise HTTPException(status_code=400, detail="InvalidProduct: Product not found")

    pricing = await validate_pricing(order.product_id)
    if not pricing:
        raise HTTPException(status_code=400, detail="PricingNotFound: No pricing found for product")
    
    price = pricing["amount"]
    discount = pricing.get("discount", 0)
    discounted_price = price * (1 - discount / 100)
    total_amount = round(order.quantity * discounted_price, 2)

    # Restore old inventory
    restored = await update_inventory(existing_order.product_id, existing_order.quantity)
    if not restored:
        raise HTTPException(status_code=400, detail="InventoryError: Failed to restore old inventory")

    # Subtract new inventory
    updated_inventory = await update_inventory(order.product_id, -order.quantity)
    if not updated_inventory:
        raise HTTPException(status_code=400, detail="InventoryError: Insufficient inventory for updated order")

    # Update DB order
    updated_order = crud.update_order(db, order_id, order, total_amount)
    return updated_order

# DELETE - Delete Order
@app.delete("/orders/{order_id}", response_model=schemas.OrderOut)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    existing_order = crud.get_order_by_id(db, order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Restore inventory
    restored = await update_inventory(existing_order.product_id, existing_order.quantity)
    if not restored:
        raise HTTPException(status_code=400, detail="InventoryError: Failed to restore inventory")

    deleted_order = crud.delete_order(db, order_id)
    return deleted_order