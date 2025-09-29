import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from order_service import models, schemas, crud, database
from typing import List
from order_service.database import SessionLocal, engine, get_db
from order_service.auth import get_oauth_token
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from fastapi import Query
from sqlalchemy import func
from order_service.models import Order


# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Order Service")

# External services
CUSTOMER_SERVICE_URL = "http://ecommerce:8000"
PRODUCT_SERVICE_URL = "http://ecommerce:8000/products"
PRICING_SERVICE_URL = "http://ecommerce:8000/pricing"
INVENTORY_SERVICE_URL = "http://ecommerce:8000/inventory"

# Helpers (sync httpx)

async def make_authenticated_request(url: str, method: str = "GET", data: dict = None):
    # Get the OAuth token
    token = await get_oauth_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url, headers=headers)
        elif method == "PUT":
            response = await client.put(url, json=data, headers=headers)
        else:
            raise HTTPException(status_code=400, detail="Unsupported HTTP method")
        
        # Handle response
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error calling {url}: {response.text}")

# Updated external service validation functions to use authenticated request
async def validate_customer(customer_id: int):
    url = f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}"
    return await make_authenticated_request(url)

# async def validate_product(product_id: int):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
#         if response.status_code == 200:
#             return response.json()
#     return None

async def validate_product(product_id: int):
    url = f"{PRODUCT_SERVICE_URL}/{product_id}"
    return await make_authenticated_request(url)

async def validate_pricing(product_id: int):
    url = f"{PRICING_SERVICE_URL}/{product_id}"
    return await make_authenticated_request(url)

async def update_inventory(product_id: int, quantity: int):
    url = f"{INVENTORY_SERVICE_URL}/{product_id}"
    current_inventory = await make_authenticated_request(url)
    
    if not current_inventory:
        return None

    current_stock = current_inventory["quantity"]
    if current_stock < quantity:
        return None

    new_quantity = current_stock - quantity
    update_payload = {"quantity": new_quantity}

    # Update the inventory with the new quantity
    return await make_authenticated_request(url, method="PUT", data=update_payload)

# Endpoints

@app.post("/orders", response_model=schemas.OrderOut)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Validate customer
    customer = await validate_customer(order.customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="InvalidCustomer: The customer ID provided is invalid.")

    # Validate product
    product = await validate_product(order.product_id)
    if not product:
        raise HTTPException(status_code=400, detail="InvalidProduct: The product ID provided is invalid.")

    # Validate pricing
    pricing = await validate_pricing(order.product_id)
    if not pricing:
        raise HTTPException(status_code=400, detail="PricingNotFound: No pricing found for product_id={order.product_id}")

    price = pricing["amount"]
    discount = pricing.get("discount", 0)
    discounted_price = price * (1 - discount / 100)
    total_amount = round(order.quantity * discounted_price, 2)

    # Update inventory
    inventory = await update_inventory(order.product_id, order.quantity)
    if not inventory:
        raise HTTPException(status_code=400, detail="InventoryError: Insufficient inventory or product not found")

    # Create the order in the database
    new_order = models.Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_amount=total_amount,
        status="Delivered"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

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


    # Save order
    # return crud.create_order(db, order, total_amount)


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
    #  Get existing order
    existing_order = crud.get_order_by_id(db, order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Validate product ID if it's changed
    if order.product_id != existing_order.product_id:
        product = await validate_product(order.product_id)
        if not product:
            raise HTTPException(status_code=400, detail="Invalid product ID")

    # Validate customer ID if it's changed
    if order.customer_id != existing_order.customer_id:
        customer = await validate_customer(order.customer_id)
        if not customer:
            raise HTTPException(status_code=400, detail="Invalid customer ID")

    # Validate pricing for the product
    pricing = await validate_pricing(order.product_id)
    if not pricing:
        raise HTTPException(status_code=400, detail="PricingNotFound: No pricing found for product")

    price = pricing["amount"]
    discount = pricing.get("discount", 0)
    discounted_price = price * (1 - discount / 100)
    total_amount = round(order.quantity * discounted_price, 2)

    # Calculate quantity difference
    if order.product_id == existing_order.product_id:
        quantity_diff = order.quantity - existing_order.quantity
        # Positive diff = customer added more → subtract from inventory
        # Negative diff = customer reduced quantity → add back to inventory
        inventory_result = await update_inventory(order.product_id, -quantity_diff)
        if "error" in inventory_result:
            raise HTTPException(status_code=400, detail=f"InventoryError: {inventory_result['error']}")
    else:
        # Product changed → restore old product inventory, subtract new product inventory
        restored = await update_inventory(existing_order.product_id, existing_order.quantity)
        if "error" in restored:
            raise HTTPException(status_code=400, detail=f"InventoryError: {restored['error']}")
        deducted = await update_inventory(order.product_id, -order.quantity)
        if "error" in deducted:
            raise HTTPException(status_code=400, detail=f"InventoryError: {deducted['error']}")

    # Update DB order
    updated_order = crud.update_order(db, order_id, order, total_amount)

    # Manually add missing fields for response
    return {
        "id": updated_order.id,
        "customer_id": updated_order.customer_id,
        "product_id": updated_order.product_id,
        "quantity": updated_order.quantity,
        "amount": price,  # Add amount here
        "discount": discount,  # Add discount here
        "total_amount": updated_order.total_amount,  # Add total_amount here
        "status": updated_order.status,
        "created_at": updated_order.created_at,
    }


# DELETE - Delete Order
@app.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    existing_order = crud.get_order_by_id(db, order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

        # Delete the order
        deleted_order = crud.delete_order(db, order_id)
        return deleted_order

    # Delete order from DB
    crud.delete_order(db, order_id)

    return JSONResponse(content={"message": "Order deleted successfully"})


@app.get("/api/frequent-users")
async def get_frequent_users(
    db: Session = Depends(get_db),
    threshold: int = Query(5, description="Minimum number of orders to consider a user frequent"),
):
    # Query to count frequent users who have >= threshold orders
    frequent_order_users = (
        db.query(Order.customer_id)
        .group_by(Order.customer_id)
        .having(func.count(Order.id) >= threshold)
        .count()
    )
    return {"frequent_order_users": frequent_order_users}


@app.get("/api/frequent-products")
async def get_frequent_products(
    db: Session = Depends(get_db),
    threshold: int = Query(10, description="Minimum number of times a product must be ordered to be considered frequent"),
):
    # Query to count frequent products that have been ordered more than the threshold number of times
    frequent_products = (
        db.query(Order.product_id)
        .group_by(Order.product_id)
        .having(func.count(Order.id) > threshold)
        .count()
    )
    return {"frequent_products": frequent_products}

"""
Today's Work Update :-
E-Commerce Product Catalog System with microservices
- Work on search service 
"""



