from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import search as crud_search
from app.schemas.search import SearchIndexCreate, SearchIndexOut
 
router = APIRouter()
 
@router.post("/", response_model=SearchIndexOut)
def create_search_index_entry(obj_in: SearchIndexCreate, db: Session = Depends(get_db)):
    return crud_search.create_search_index(db, obj_in)
 
@router.get("/{search_id}", response_model=SearchIndexOut)
def read_search_index(search_id: int, db: Session = Depends(get_db)):
    obj = crud_search.get_search_index(db, search_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Search entry not found")
    return obj
 
@router.get("/", response_model=list[SearchIndexOut])
def list_search_indices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_search.get_all_search_indices(db, skip, limit)
 
@router.get("/search/", response_model=list[SearchIndexOut])
def search_entries(query: str, db: Session = Depends(get_db)):
    return crud_search.search_by_name(db, query)
 
@router.delete("/{search_id}")
def delete_search_index(search_id: int, db: Session = Depends(get_db)):
    obj = crud_search.get_search_index(db, search_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Search entry not found")
   
    crud_search.delete_search_index(db, obj)
   
    return {"message": f"Search entry with ID {search_id} deleted successfully."}
 