from sqlalchemy.orm import Session
from app.models.search import SearchIndex
from app.schemas.search import SearchIndexCreate, SearchIndexUpdate


def create_search_entry(db: Session, obj_in: SearchIndexCreate):
    db_obj = SearchIndex(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_search_entry(db: Session, entry_id: int):
    return db.query(SearchIndex).filter(SearchIndex.id == entry_id).first()


def get_search_results(db: Session, query: str):
    return db.query(SearchIndex).filter(
        (SearchIndex.name.ilike(f"%{query}%")) |
        (SearchIndex.description.ilike(f"%{query}%")) |
        (SearchIndex.category.ilike(f"%{query}%"))
    ).all()


def update_search_entry(db: Session, entry_id: int, obj_in: SearchIndexUpdate):
    db_obj = get_search_entry(db, entry_id)
    if not db_obj:
        return None
    update_data = obj_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_search_entry(db: Session, entry_id: int):
    db_obj = get_search_entry(db, entry_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False
