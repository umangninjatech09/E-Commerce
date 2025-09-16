from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductOut, ProductUpdate, ProductWithInventory
from app.crud.product import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
    get_product_by_sku,
    get_product
)
from app.db.session import get_db
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.pricing import Pricing
from app.utils.response_builder import error_response

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/all", response_model=List[ProductWithInventory])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    result = []
    for product in products:
        inventory = db.query(Inventory).filter(Inventory.product_id == product.id).first()
        pricing = db.query(Pricing).filter(Pricing.product_id == product.id).first()

        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "sku": product.sku,
            "category": product.category,
            "brand": product.brand,
            "created_at": product.created_at,
            "quantity": inventory.quantity if inventory else 0,
            "amount": pricing.amount if pricing else 0.0
        })
    return result

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def api_create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    existing = get_product_by_sku(db, payload.sku)
    if existing:
        return error_response(400, "DuplicateSKU", "A product with this SKU already exists.")
    return create_product(db, payload)

@router.get("/", response_model=List[ProductOut])
def api_list_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def api_get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        return error_response(404, "ProductNotFound", f"Product with id {product_id} not found.")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def api_update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, payload)
    if not product:
        return error_response(404, "ProductNotFound", f"Cannot update: product with id {product_id} was not found.")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def api_delete_product(product_id: int, db: Session = Depends(get_db)):
    product = delete_product(db, product_id)
    if not product:
        return error_response(404, "ProductNotFound", f"Cannot delete: product with id {product_id} was not found.")
    return {"message": "Product deleted successfully"}