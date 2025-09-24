import httpx
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from order_service import models, schemas, crud, database
from order_service.database import get_db
from typing import List

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Order Service")

# External services URLs
CUSTOMER_SERVICE_URL = "http://127.0.0.1:8000"
PRODUCT_SERVICE_URL = "http://127.0.0.1:8000/products"
PRICING_SERVICE_URL = "http://127.0.0.1:8000/pricing"
INVENTORY_SERVICE_URL = "http://127.0.0.1:8000/inventory"


# Dependency to extract the JWT token from the Authorization header
async def get_token(authorization: str = Header(...)):
    if authorization.startswith("Bearer "):
        return authorization[7:]  # Return the token after 'Bearer '
    else:
        raise HTTPException(status_code=403, detail="Invalid or missing token")


# Helpers (sync httpx) for external service calls

async def validate_customer(customer_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}", headers=headers)
        if response.status_code == 200:
            return response.json()
    return None

async def validate_product(product_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/{product_id}", headers=headers)
        if response.status_code == 200:
            return response.json()
    return None

async def validate_pricing(product_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRICING_SERVICE_URL}/{product_id}", headers=headers)
        if response.status_code == 200:
            return response.json()
    return None

async def update_inventory(product_id: int, quantity: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{INVENTORY_SERVICE_URL}/{product_id}", headers=headers)
            if response.status_code != 200:
                return None

            inventory = response.json()
            current_stock = inventory["quantity"]

            if current_stock < quantity:
                return None

            new_quantity = current_stock - quantity
            update_payload = {"quantity": new_quantity}

            put_response = await client.put(
                f"{INVENTORY_SERVICE_URL}/{product_id}", json=update_payload, headers=headers
            )
            if put_response.status_code == 200:
                return put_response.json()

        except Exception as e:
            print(f"Error updating inventory: {str(e)}")
    return None


# Endpoints

@app.post("/orders", response_model=schemas.OrderOut)
async def create_order(
    order: schemas.OrderCreate,
    token: str = Depends(get_token),  # Get the token from the Authorization header
    db: Session = Depends(get_db)
):
    # Validate customer
    customer = await validate_customer(order.customer_id, token)
    if not customer:
        raise HTTPException(status_code=400, detail="Invalid Customer")

    # Validate product
    product = await validate_product(order.product_id, token)
    if not product:
        raise HTTPException(status_code=400, detail="Invalid Product", detail="The product ID provided is invalid.")

    # Validate pricing
    pricing = await validate_pricing(order.product_id, token)
    if not pricing:
        raise HTTPException(status_code=400, detail="Pricing Not Found", detail=f"No pricing found for product_id={order.product_id}")

    price = pricing["amount"]
    discount = pricing.get("discount", 0)

    discounted_price = price * (1 - discount / 100)
    total_amount = round(order.quantity * discounted_price, 2)

    # Update inventory
    inventory = await update_inventory(order.product_id, order.quantity, token)
    if not inventory:
        raise HTTPException(status_code=400, detail="InventoryError", detail="Insufficient inventory or product not found")

    new_order = models.Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_amount=total_amount,
        status="delivered"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Manually add amount & discount for response
    return {
        "id": new_order.id,
        "customer_id": new_order.customer_id,
        "product_id": new_order.product_id,
        "quantity": new_order.quantity,
        "amount": price,
        "discount": discount,
        "total_amount": new_order.total_amount,
        "status": new_order.status,
        "created_at": new_order.created_at,
    }


@app.get("/orders", response_model=List[schemas.OrderOut])
async def list_orders(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    # Fetch all orders from the database
    db_orders = crud.get_orders(db)

    # Prepare the response with amount, discount, and total_amount for each order
    orders_with_details = []
    for db_order in db_orders:
        # Fetch pricing info for each product in the order
        pricing = await validate_pricing(db_order.product_id, token)
        if not pricing:
            raise HTTPException(status_code=400, detail=f"Pricing not found for product {db_order.product_id}")

        price = pricing["amount"]
        discount = pricing.get("discount", 0)

        # Calculate the original amount (price * quantity before discount)
        original_amount = price * db_order.quantity

        # Calculate the discounted total amount (price * quantity * (1 - discount / 100))
        discounted_price = original_amount * (1 - discount / 100)
        total_amount = round(discounted_price, 2)

        # Append the order details with the pricing information
        orders_with_details.append(schemas.OrderOut(
            id=db_order.id,
            customer_id=db_order.customer_id,
            product_id=db_order.product_id,
            quantity=db_order.quantity,
            total_amount=total_amount,
            amount=original_amount,
            discount=discount,
            status=db_order.status,               
            created_at=db_order.created_at              
        ))

    return orders_with_details


@app.put("/orders/{order_id}", response_model=schemas.OrderOut)
async def update_order(
    order_id: int, 
    order: schemas.OrderUpdate,
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    existing_order = crud.get_order_by_id(db, order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.product_id != existing_order.product_id:
        product = await validate_product(order.product_id, token)
        if not product:
            raise HTTPException(status_code=400, detail="Invalid product ID")

    if order.customer_id != existing_order.customer_id:
        customer = await validate_customer(order.customer_id, token)
        if not customer:
            raise HTTPException(status_code=400, detail="Invalid customer ID")

    pricing = await validate_pricing(order.product_id, token)
    if not pricing:
        raise HTTPException(status_code=400, detail="Pricing not found")

    price = pricing["amount"]
    discount = pricing.get("discount", 0)
    discounted_price = price * (1 - discount / 100)
    total_amount = round(order.quantity * discounted_price, 2)

    # Adjust inventory: restore old, subtract new
    restore_inventory = await update_inventory(existing_order.product_id, -existing_order.quantity, token)
    if not restore_inventory:
        raise HTTPException(status_code=400, detail="Failed to restore old inventory")

    inventory = await update_inventory(order.product_id, order.quantity, token)
    if not inventory:
        raise HTTPException(status_code=400, detail="Insufficient inventory for updated order")

    # Update order in DB
    updated_order = crud.update_order(db, order_id, order, total_amount)
    return updated_order


@app.delete("/orders/{order_id}", response_model=schemas.OrderOut)
async def delete_order(
    order_id: int, 
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    existing_order = crud.get_order_by_id(db, order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Restore inventory
    restore_inventory = await update_inventory(existing_order.product_id, -existing_order.quantity, token)
    if not restore_inventory:
        raise HTTPException(status_code=400, detail="Failed to restore inventory after deletion")

    # Delete order
    deleted_order = crud.delete_order(db, order_id)
    return deleted_order
