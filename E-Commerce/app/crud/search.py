from sqlalchemy.orm import Session
from app.models import search as models
from app.schemas import search as schemas
from typing import List, Optional

def create_or_update_index(db: Session, data: schemas.SearchIndexIn):
    existing = db.query(models.SearchIndex).filter(models.SearchIndex.product_id == data.product_id).first()
    if existing:
        for field, value in data.dict().items():
            setattr(existing, field, value)
        db.commit()          # Save changes permanently
        db.refresh(existing) # Refresh object with latest DB state
        return existing
    else:
        new_entry = models.SearchIndex(**data.dict())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry

def search_products(db: Session, q: Optional[str] = None, category: Optional[str] = None,
                    min_price: Optional[float] = None, max_price: Optional[float] = None,
                    stock_status: Optional[str] = None, sort_by: Optional[str] = None,
                    order: str = "asc") -> List[models.SearchIndex]:
    query = db.query(models.SearchIndex)

    if q:
        query = query.filter((models.SearchIndex.name.contains(q))|(models.SearchIndex.description.contains(q)))
    if category:
        query = query.filter(models.SearchIndex.category == category)
    if min_price is not None:
        query = query.filter(models.SearchIndex.price >= min_price)
    if max_price is not None:
        query = query.filter(models.SearchIndex.price <= max_price)
    if stock_status:
        query = query.filter(models.SearchIndex.stock_status == stock_status)

    if sort_by:
        if order == "asc":
            query = query.order_by(getattr(models.SearchIndex, sort_by).asc())
        else:
            query = query.order_by(getattr(models.SearchIndex, sort_by).desc())

    return query.all()

def update_index(db: Session, product_id: int, data: schemas.SearchIndexIn):
    db_index = db.query(models.SearchIndex).filter(models.SearchIndex.product_id == product_id).first()
    if not db_index:
        return None  
    for field, value in data.dict().items():
        setattr(db_index, field, value)
    db.commit()
    db.refresh(db_index)
    return db_index

def get_index_by_id(db: Session, product_id: int):
    return db.query(models.SearchIndex).filter(models.SearchIndex.product_id == product_id).first()

def delete_index(db: Session, product_id: int) -> bool:
    db_index = db.query(models.SearchIndex).filter(models.SearchIndex.product_id == product_id).first()
    if db_index:
        db.delete(db_index)
        db.commit()
        return True
    return False