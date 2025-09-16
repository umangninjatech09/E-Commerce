from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.search import SearchCreate, SearchUpdate, SearchOut
from app.crud import search as crud_search

router = APIRouter(prefix="/search", tags=["Search"])


# Create Search Entry
@router.post("/", response_model=SearchOut)
def create_search(search: SearchCreate, db: Session = Depends(get_db)):
    entry = crud_search.create_search_index(db, search)
    return entry


# Get Search Entry by product_id
@router.get("/{product_id}", response_model=SearchOut)
def read_search(product_id: int, db: Session = Depends(get_db)):
    entry = crud_search.get_search_index(db, product_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Search entry not found")
    return entry


# Update Search Entry
@router.put("/{product_id}", response_model=SearchOut)
def update_search(product_id: int, search: SearchUpdate, db: Session = Depends(get_db)):
    entry = crud_search.update_search_index(db, product_id, search)
    if not entry:
        raise HTTPException(status_code=404, detail="Search entry not found")
    return entry


#Delete Search Entry
@router.delete("/{product_id}")
def delete_search(product_id: int, db: Session = Depends(get_db)):
    entry = crud_search.delete_search_index(db, product_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Search entry not found")
    return {"message": "Deleted successfully"}


# Get All Entries
@router.get("/", response_model=List[SearchOut])
def get_all(db: Session = Depends(get_db)):
    return crud_search.get_all_search_entries(db)


# Search by Keyword
@router.get("/keyword/{keyword}", response_model=List[SearchOut])
def search_keyword(keyword: str, db: Session = Depends(get_db)):
    return crud_search.search_entries(db, keyword)


# Get by Entity Type + ID
@router.get("/entity/{entity_type}/{entity_id}", response_model=SearchOut)
def search_by_entity(entity_type: str, entity_id: int, db: Session = Depends(get_db)):
    entry = crud_search.get_by_entity(db, entity_type, entity_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entity not found in search index")
    return entry
