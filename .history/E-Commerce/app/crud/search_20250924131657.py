from sqlalchemy.orm import Session
from app.models.search import SearchIndex
from app.schemas.search import SearchIndexCreate
 
def create_search_index(db: Session, obj_in: SearchIndexCreate):
    db_obj = SearchIndex(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
 
def get_search_index(db: Session, search_id: int):
    return db.query(SearchIndex).filter(SearchIndex.id == search_id).first()
 
def get_all_search_indices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SearchIndex).offset(skip).limit(limit).all()
 
# def search_by_name(db: Session, query: str):
#     return db.query(SearchIndex).filter(SearchIndex.name.ilike(f"%{query}%")).all()
 
def search_by_name(db, query: str):
    results = db.query(SearchIndex).all()
    return [r for r in results if r.product_name and query.lower() in r.product_name.lower()]
 

def delete_search_index(db: Session, obj: SearchIndex):
    db.delete(obj)
    db.commit()
 
 """
 - Work on search-ser
 """