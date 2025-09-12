from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.crud.product import (
    get_product_by_id,
    get_product_by_name,
    get_all_products,
    create_product,
    update_product,
    delete_product,
    get_all_product,
)

router = APIRouter()


# -------------------- CREATE PRODUCT -------------------- #
@router.post("/", response_model=ProductOut)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    existing_product = get_product_by_name(db, product.name)
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    return create_product(db, product)


# -------------------- GET PRODUCT BY ID -------------------- #
@router.get("/{product_id}", response_model=ProductOut)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# -------------------- LIST PRODUCTS -------------------- #
@router.get("/", response_model=List[ProductOut])
def list_products_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_products(db, skip=skip, limit=limit)


# -------------------- UPDATE PRODUCT -------------------- #
@router.put("/{product_id}", response_model=ProductOut)
def update_product_endpoint(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# -------------------- DELETE PRODUCT -------------------- #
@router.delete("/{product_id}", response_model=ProductOut)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    db_product = delete_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/all", response_model=List[Product])
def get_all_product_endpoint(db: Session = Depends(get_db)):
    return get_all_product(db)