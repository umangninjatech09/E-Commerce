from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.search import SearchIndexIn, SearchIndexOut
from app.crud import search as crud
from app.db.session import get_db

router = APIRouter()

@router.post("/index", response_model=SearchIndexOut)
def index_product(data: SearchIndexIn, db: Session = Depends(get_db)):
    return crud.create_or_update_index(db, data)

@router.get("/", response_model=List[SearchIndexOut])
def search_products_endpoint(
    q: Optional[str] = Query(None, description="Keyword to search in name or description"),
    category: Optional[str] = Query(None, description="Filter by product category"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    stock_status: Optional[str] = Query(None, description="Filter by stock status (yes/no)"),
    sort_by: Optional[str] = Query(
        None,
        description="Sort by field: 'price' or 'rating'",
        regex="^(price|rating)?$"
    ),
    order: str = Query(
        "asc",
        description="Sort order: 'asc' or 'desc'",
        regex="^(asc|desc)$"
    ),
    db: Session = Depends(get_db),
):
    return crud.search_products(
        db=db,
        q=q,
        category=category,
        min_price=min_price,
        max_price=max_price,
        stock_status=stock_status,
        sort_by=sort_by,
        order=order
    )

# PUT product by Id
@router.put("/{product_id}", response_model=SearchIndexOut)
def update_product(product_id: int, data: SearchIndexIn, db: Session = Depends(get_db)):
    updated_product = crud.update_index(db, product_id, data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

# Get product by ID
@router.get("/{product_id}", response_model=SearchIndexOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_index_by_id(db, product_id)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Delete product by Id
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_index(db, product_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True}