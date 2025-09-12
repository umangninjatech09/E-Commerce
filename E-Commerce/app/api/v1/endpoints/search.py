from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.search import SearchIndexCreate, SearchIndexUpdate, SearchIndexOut
from app.crud import search as crud


router = APIRouter()


@router.post("/", response_model=SearchIndexOut)
def create_entry(entry: SearchIndexCreate, db: Session = Depends(get_db)):
    return crud.create_search_entry(db, entry)


@router.get("/{entry_id}", response_model=SearchIndexOut)
def read_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = crud.get_search_entry(db, entry_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return db_entry


@router.get("/search/", response_model=List[SearchIndexOut])
def search_entries(q: str, db: Session = Depends(get_db)):
    return crud.get_search_results(db, q)


@router.put("/{entry_id}", response_model=SearchIndexOut)
def update_entry(entry_id: int, entry: SearchIndexUpdate, db: Session = Depends(get_db)):
    db_entry = crud.update_search_entry(db, entry_id, entry)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return db_entry


@router.delete("/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    success = crud.delete_search_entry(db, entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"ok": True}
