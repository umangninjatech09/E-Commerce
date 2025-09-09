from sqlalchemy.orm import Session
from app.models import pricing as models
from app.schemas import pricing as schemas  
from typing import List

# ---------------- Price CRUD ---------------- #

def create_or_update_price(db: Session, data: schemas.PriceCreate):
    db_price = db.query(models.Price).filter(models.Price.product_id == data.product_id).first()
    if db_price:
        db_price.base_price = data.base_price
    else:
        db_price = models.Price(
            product_id=data.product_id,
            base_price=data.base_price
        )
        db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

def get_price_by_product(db: Session, product_id: str):
    return db.query(models.Price).filter(models.Price.product_id == product_id).first()

def get_all_prices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Price).offset(skip).limit(limit).all()

def delete_price(db: Session, product_id: str):
    db_price = db.query(models.Price).filter(models.Price.product_id == product_id).first()
    if db_price:
        db.delete(db_price)
        db.commit()
        return True
    return False

# Discount CRUD 



def get_discounts_by_product(db: Session, product_id: str) -> List[models.Discount]:
    return db.query(models.Discount).filter(models.Discount.product_id == product_id).all()

def delete_discount(db: Session, discount_id: int):
    db_discount = db.query(models.Discount).filter(models.Discount.id == discount_id).first()
    if db_discount:
        db.delete(db_discount)
        db.commit()
        return True
    return False


# def create_or_update_price(db: Session, data: schemas.PriceCreate):
#     db_price = db.query(models.Price).filter(models.Price.product_id == data.product_id).first()
#     if db_price:
#         db_price.base_price = data.base_price
#     else:
#         db_price = models.Price(product_id=data.product_id, base_price=data.base_price)
#         db.add(db_price)
#     db.commit()
#     db.refresh(db_price)  # <--- Ensure created_at is loaded
#     return db_price


def create_or_update_discount(db: Session, data: schemas.DiscountCreate):
    db_discount = models.Discount(
        product_id=data.product_id,
        discount_percentage=data.discount_percentage,
        start_date=data.start_date,
        end_date=data.end_date,
        # created_at=datetime.utcnow()  # <--- Assign created_at explicitly
    )
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)  # <--- Ensure created_at is loaded
    return db_discount