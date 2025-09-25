import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from order_service import models, schemas, crud, database
from typing import List
from order_service.database import SessionLocal, engine, get_db
from order_service.auth import get_oauth_token
from fastapi.responses import JSONResponse
from fastapi import APIRouter
 
 
# Create tables
models.Base.metadata.create_all(bind=database.engine)
 
app = FastAPI(title="Order Service")
 
# External services
CUSTOMER_SERVICE_URL = "http://localhost:8000"
PRODUCT_SERVICE_URL = "http://localhost:8000/products"
PRICING_SERVICE_URL = "http://localhost:8000/pricing"
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
 
 
@app.get("/orders", response_model=List[schemas.OrderOut])
async def list_orders(db: Session = Depends(get_db)):
    # Fetch all orders from the database
    db_orders = crud.get_orders(db)
 
    # Prepare the response with amount, discount, and total_amount for each order
    orders_with_details = []
    for db_order in db_orders:
        # Fetch pricing info for each product in the order
        pricing = await validate_pricing(db_order.product_id)
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
async def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=400, detail="Pricing not found")
 
    price = pricing["amount"]
    discount = pricing.get("discount", 0)
    discounted_price = price * (1 - discount / 100)
    total_amount = round(order.quantity * discounted_price, 2)
 
    # Adjust inventory: restore old, subtract new
    restore_inventory = await update_inventory(existing_order.product_id, -existing_order.quantity)
    if not restore_inventory:
        raise HTTPException(status_code=400, detail="Failed to restore old inventory")
 
    inventory = await update_inventory(order.product_id, order.quantity)
    if not inventory:
        raise HTTPException(status_code=400, detail="Insufficient inventory for updated order")
 
    # Update order in DB
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
 
    # Restore inventory
    restore_inventory = await update_inventory(existing_order.product_id, -existing_order.quantity)
    if not restore_inventory:
        raise HTTPException(status_code=400, detail="Failed to restore inventory after deletion")
 
    # Delete order from DB
    crud.delete_order(db, order_id)
 
    return JSONResponse(content={"message": "Order deleted successfully"})
 
 
 
 
 
 
 
 
 
 