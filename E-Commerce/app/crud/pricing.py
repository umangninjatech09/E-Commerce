from sqlalchemy.orm import Session
from app.models.pricing import Pricing
from app.schemas.pricing import PricingCreate

def create_pricing(db: Session, pricing: PricingCreate):
    db_pricing = Pricing(**pricing.dict())
    db.add(db_pricing)
    db.commit()
    db.refresh(db_pricing)
    return db_pricing

def get_all_pricings(db: Session):
    return db.query(Pricing).all()

def get_pricing_by_id(db: Session, pricing_id: int):
    return db.query(Pricing).filter(Pricing.id == pricing_id).first()

def get_pricing_by_product(db: Session, product_id: int):
    return db.query(Pricing).filter(Pricing.product_id == product_id).first()

def update_pricing(db: Session, pricing_id: int, pricing: PricingCreate):
    db_pricing = get_pricing_by_id(db, pricing_id)
    if not db_pricing:
        return None
    for key, value in pricing.dict().items():
        setattr(db_pricing, key, value)
    db.commit()
    db.refresh(db_pricing)
    return db_pricing

def delete_pricing(db: Session, pricing_id: int):
    db_pricing = get_pricing_by_id(db, pricing_id)
    if db_pricing:
        db.delete(db_pricing)
        db.commit()
        return True
    return False