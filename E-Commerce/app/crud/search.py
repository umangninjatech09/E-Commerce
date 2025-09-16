from sqlalchemy.orm import Session
from app.models.search import SearchIndex
from app.schemas.search import SearchCreate, SearchUpdate
from typing import List, Optional


# ✅ Create (with duplicate check)
def create_search_index(db: Session, search: SearchCreate) -> SearchIndex:
    existing = db.query(SearchIndex).filter(SearchIndex.product_id == search.product_id).first()
    if existing:
        return existing  

    entry = SearchIndex(**search.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


# ✅ Read (by product_id)
def get_search_index(db: Session, product_id: int) -> Optional[SearchIndex]:
    return db.query(SearchIndex).filter(SearchIndex.product_id == product_id).first()


# ✅ Update (by product_id)
def update_search_index(db: Session, product_id: int, search: SearchUpdate) -> Optional[SearchIndex]:
    entry = db.query(SearchIndex).filter(SearchIndex.product_id == product_id).first()
    if not entry:
        return None
    for key, value in search.dict(exclude_unset=True).items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry


# ✅ Delete (by product_id)
def delete_search_index(db: Session, product_id: int) -> Optional[SearchIndex]:
    entry = db.query(SearchIndex).filter(SearchIndex.product_id == product_id).first()
    if entry:
        db.delete(entry)
        db.commit()
    return entry


# ✅ Get all entries
def get_all_search_entries(db: Session) -> List[SearchIndex]:
    return db.query(SearchIndex).all()


# ✅ Search by keyword (name, description, category)
def search_entries(db: Session, keyword: str) -> List[SearchIndex]:
    return db.query(SearchIndex).filter(
        (SearchIndex.name.ilike(f"%{keyword}%")) |
        (SearchIndex.description.ilike(f"%{keyword}%")) |
        (SearchIndex.category.ilike(f"%{keyword}%"))
    ).all()


# ✅ Get by entity type (customer, inventory, pricing, product)
def get_by_entity(db: Session, entity_type: str, entity_id: int) -> Optional[SearchIndex]:
    return db.query(SearchIndex).filter(
        SearchIndex.entity_type == entity_type,
        SearchIndex.entity_id == entity_id
    ).first()