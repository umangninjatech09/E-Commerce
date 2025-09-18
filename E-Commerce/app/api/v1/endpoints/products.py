from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.crud import product as crud_product
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate, ProductPagination
from app.crud.product import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
    get_product_by_sku,
)
from app.db.session import get_db
from app.utils.response_builder import error_response
from fastapi import Query
from app.utils.pagination import paginate
from app.schemas.common import Page


<<<<<<< HEAD
router = APIRouter(prefix="/products", tags=["Products"])
=======
router = APIRouter(tags=["Products"])
>>>>>>> feature/purchase-service

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def api_create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    existing = get_product_by_sku(db, payload.sku)
    if existing:
        return error_response(400, "DuplicateSKU", "A product with this SKU already exists.")
    return create_product(db, payload)

@router.get("/", response_model=Page[ProductOut])
def api_list_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    query = db.query(Product)
    return paginate(query, page, size)

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


@router.get("/products/", response_model=ProductPagination)
def get_products(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    total, products = crud_product.get_products(db, skip=(page-1)*limit, limit=limit)
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    # Validate page number
    if page < 1 or page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid page number. Total available pages: {total_pages}"
        )

    # Calculate previous and next page numbers
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    # Return structured pagination response
    return {
        "total_records": total,
        "total_pages": total_pages,
        "current_page": page,
        "prev_page": prev_page,
        "next_page": next_page,
        "limit": limit,
        "items": products
    }