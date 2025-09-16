from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.search import SearchCreate, SearchUpdate, SearchOut
from app.crud import search as crud_search

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/", response_model=SearchOut)
def create_search(search: SearchCreate, db: Session = Depends(get_db)):
    return crud_search.create_search_index(db, search)

@router.get("/", response_model=list[SearchOut])
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

@router.get("/search-text/{query}", response_model=List[SearchOut])
def search_text(query: str, db: Session = Depends(get_db)):
    return crud_search.search_text(db, query)