from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.schemas.search import SearchCreate, SearchUpdate, SearchOut
from app.crud import search as crud_search

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/", response_model=SearchOut)
def create_search(search: SearchCreate, db: Session = Depends(get_db)):
    return crud_search.create_search_index(db, search)

@router.get("/", response_model=ist[SearchOut])
def read_search(db: Session = Depends(get_db)):
    return crud_search.get_all_search_indexes(db)

@router.get("/{product_id}", response_model=SearchOut)
def read_search(product_id: int, db: Session = Depends(get_db)):
    entry = crud_search.get_search_index(db, product_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Search entry not found")
    return entry

@router.put("/{product_id}", response_model=SearchOut)
def update_search(product_id: int, search: SearchUpdate, db: Session = Depends(get_db)):
    entry = crud_search.update_search_index(db, product_id, search)
    if not entry:
        raise HTTPException(status_code=404, detail="Search entry not found")
    return entry

@router.delete("/{id}")
def delete_search(id: int, db: Session = Depends(get_db)):
    success = crud_search.delete_search_index(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Search entry not found")
    return {"message": "Deleted successfully"}

@router.get("/search-text/", response_model=list[SearchOut])
def search_text(
    q: str = Query(..., description="Search keyword"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    db: Session = Depends(get_db),
):
    return crud_search.search_text(db, query=q, min_price=min_price, max_price=max_price)