from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, product_in: ProductCreate) -> Product:
    db_product = Product(**product_in.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session) -> List[Product]:
    return db.query(Product).order_by(Product.id).all()

def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
    return db.query(Product).filter(Product.sku == sku).first()

def update_product(db: Session, product_id: int, product_in: ProductUpdate) -> Optional[Product]:
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    update_data = product_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> Optional[Product]:
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product

get
