from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import pricing as crud_pricing
from app.schemas import pricing as schemas
from app.db.session import get_db
from typing import List
from app.utils.response_builder import error_response
from app.models.product import Product
<<<<<<< HEAD
from app.schemas.pricing import PricingPagination

router = APIRouter(
    prefix="/pricing",
    tags=["Pricing"]
)
=======
from fastapi import Query
from app.utils.pagination import paginate
from app.schemas.common import Page
from app.models.pricing import Pricing



router = APIRouter(tags=["Pricing"])
>>>>>>> feature/purchase-service

@router.post("/", response_model=schemas.Pricing)
def api_create_pricing(pricing: schemas.PricingCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == pricing.product_id).first()
    if not product:
        return error_response(404, "ProductNotFound", f"Cannot create pricing: product_id={pricing.product_id} does not exist.")
    return crud_pricing.create_pricing(db, pricing)

@router.get("/", response_model=Page[schemas.Pricing])
def api_list_pricings(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    query = db.query(Pricing)
    return paginate(query, page, size)

@router.get("/{pricing_id}", response_model=schemas.Pricing)
def api_get_pricing(pricing_id: int, db: Session = Depends(get_db)):
    db_pricing = crud_pricing.get_pricing_by_id(db, pricing_id)
    if not db_pricing:
        return error_response(404, "PricingNotFound", f"Pricing with id {pricing_id} not found.")
    return db_pricing

@router.get("/product/{product_id}", response_model=schemas.Pricing)
def get_pricing_by_product(product_id: int, db: Session = Depends(get_db)):
    db_pricing = crud_pricing.get_pricing_by_product(db, product_id)
    if not db_pricing:
        return error_response(404, "PricingNotFound", f"Pricing for product_id {product_id} not found.")
    return db_pricing

@router.put("/{pricing_id}", response_model=schemas.Pricing)
def update_pricing(pricing_id: int, data: schemas.PricingCreate, db: Session = Depends(get_db)):
    db_pricing = crud_pricing.update_pricing(db, pricing_id, data)
    if not db_pricing:
        return error_response(404, "PricingNotFound", f"Cannot update: pricing record with id={pricing_id} was not found.")
    return db_pricing

@router.delete("/{pricing_id}")
def delete_pricing(pricing_id: int, db: Session = Depends(get_db)):
    deleted = crud_pricing.delete_pricing(db, pricing_id)
    if not deleted:
        return error_response(404, "PricingNotFound", f"Cannot delete: pricing record with id={pricing_id} was not found.")
    return {"detail": "Pricing deleted successfully"}

@router.get("/products/", response_model=PricingPagination)
def get_pricing_limit(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    total, products = crud_pricing.get_pricing_limit(db, skip=(page-1)*limit, limit=limit)
    
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
