from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import pricing as crud_pricing
from app.schemas import pricing as schemas
from app.db.session import get_db
from 

router = APIRouter(
    prefix="/pricing",
    tags=["Pricing"]
)

@router.post("/", response_model=schemas.Pricing)
def api_create_pricing(pricing: schemas.PricingCreate, db: Session = Depends(get_db)):
    return crud_pricing.create_pricing(db, pricing)

@router.get("/", response_model=list[schemas.Pricing])
def api_list_pricings(db: Session = Depends(get_db)):
    return crud_pricing.get_all_pricings(db)

@router.get("/{pricing_id}", response_model=schemas.Pricing)
def api_get_pricing(pricing_id: int, db: Session = Depends(get_db)):
    db_pricing = crud_pricing.get_pricing_by_id(db, pricing_id)
    if not db_pricing:
        raise HTTPException(status_code=404, detail="Pricing not found")
    return db_pricing

@router.get("/product/{product_id}", response_model=schemas.Pricing)
def get_pricing_by_product(product_id: int, db: Session = Depends(get_db)):
    db_pricing = crud_pricing.get_pricing_by_product(db, product_id)
    if not db_pricing:
        raise HTTPException(status_code=404, detail="Pricing not found")
    return db_pricing

@router.put("/{pricing_id}", response_model=schemas.Pricing)
def update_pricing(pricing_id: int, data: schemas.PricingCreate, db: Session = Depends(get_db)):
    db_pricing = crud_pricing.update_pricing(db, pricing_id, data)
    if not db_pricing:
        raise HTTPException(status_code=404, detail="Pricing not found")
    return db_pricing

@router.delete("/{pricing_id}")
def delete_pricing(pricing_id: int, db: Session = Depends(get_db)):
    deleted = crud_pricing.delete_pricing(db, pricing_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Pricing not found")
    return {"detail": "Pricing deleted successfully"}