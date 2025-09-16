from sqlalchemy.orm import Session
from app.models.search import SearchIndex
from app.models.product import Product
from app.models.customer import Customer
from app.models.inventory import Inventory
from app.models.pricing import Pricing
from app.schemas.search import SearchCreate, SearchUpdate

def get_all_search_indexes(db: Session):
    return db.query(SearchIndex).all()

def create_search_index(db: Session, search: SearchCreate):
    db_entry = SearchIndex(**search.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_search_index(db: Session, product_id: int):
    entry = db.query(SearchIndex).filter(SearchIndex.product_id == product_id).first()
    if entry:
        entry.product = entry.product or db.query(Product).filter(Product.id == entry.product_id).first()
        entry.customer = entry.customer or db.query(Customer).filter(Customer.id == entry.customer_id).first()
        entry.inventory = entry.inventory or db.query(Inventory).filter(Inventory.id == entry.inventory_id).first()
        entry.pricing = entry.pricing or db.query(Pricing).filter(Pricing.id == entry.pricing_id).first()
    return entry

def update_search_index(db: Session, product_id: int, search: SearchUpdate):
    entry = db.query(SearchIndex).filter(SearchIndex.product_id == product_id).first()
    if not entry:
        return None
    for key, value in search.dict(exclude_unset=True).items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry

def delete_search_index(db: Session, id: int):
    entry = db.query(SearchIndex).filter(SearchIndex.id == id).first()
    if not entry:
        return False
    db.delete(entry)
    db.commit()
    return True

def search_text(db: Session, query: str):
    entries = db.query(SearchIndex).filter(SearchIndex.name.ilike(f"%{query}%")).all()
    for e in entries:
        e.product = e.product or db.query(Product).filter(Product.id == e.product_id).first()
        e.customer = e.customer or db.query(Customer).filter(Customer.id == e.customer_id).first()
        e.inventory = e.inventory or db.query(Inventory).filter(Inventory.id == e.inventory_id).first()
        e.pricing = e.pricing or db.query(Pricing).filter(Pricing.id == e.pricing_id).first()
    return entries

