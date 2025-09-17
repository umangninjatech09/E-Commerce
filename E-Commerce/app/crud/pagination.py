from sqlalchemy.orm import Session
from typing import Type, Tuple

def get_items_paginated(db: Session, model: Type, skip: int = 0, limit: int = 10) -> Tuple[int, list]:
    """
    Generic function to fetch items from any SQLAlchemy model with pagination.
    Returns total count and list of items.
    """
    query = db.query(model)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return total, items
