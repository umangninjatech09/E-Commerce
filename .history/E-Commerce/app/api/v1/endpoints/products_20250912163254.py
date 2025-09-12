from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.crud.product import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
    get_product_by_sku,
)
from app.db.session import get_db

router = APIRouter(prefix="/products", tags=["Products"])





@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def api_create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    existing = get_product_by_sku(db, payload.sku)
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    return create_product(db, payload)

@router.get("/", response_model=List[ProductOut])
def api_list_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def api_get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def api_update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def api_delete_product(product_id: int, db: Session = Depends(get_db)):
    product = delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
