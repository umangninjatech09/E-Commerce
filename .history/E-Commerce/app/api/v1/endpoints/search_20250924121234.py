from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import search as crud_search
from app.schemas.search import SearchIndexCreate, SearchIndexOut
from typing import List 
from app.utils.response_builder import error_response
from app.models.product import Product
from app.models.customer import Customer
from app.models.inventory import Inventory
from app.models.pricing import Pricing


router = APIRouter()
 
@router.post("/", response_model=SearchIndexOut)
def create_search_index_entry(obj_in: SearchIndexCreate, db: Session = Depends(get_db)):
    # check product
    product = db.query(Product).filter(Product.id == obj_in.product_id).first()
    if not product:
        return error_response(404, "ProductNotFound", f"Cannot create: product with id {obj_in.product_id} was not found.")

    # check customer
    customer = db.query(Customer).filter(Customer.id == obj_in.customer_id).first()
    if not customer:
        return error_response(404, "CustomerNotFound", f"Cannot create: customer with id {obj_in.customer_id} was not found.")

    # check inventory
    inventory = db.query(Inventory).filter(Inventory.id == obj_in.inventory_id).first()
    if not inventory:
        return error_response(404, "InventoryNotFound", f"Cannot create: inventory with id {obj_in.inventory_id} was not found.")

    # check pricing
    pricing = db.query(Pricing).filter(Pricing.id == obj_in.pricing_id).first()
    if not pricing:
        return error_response(404, "PricingNotFound", f"Cannot create: pricing with id {obj_in.pricing_id} was not found.")

    # ✅ all checks passed → create entry
    return crud_search.create_search_index(db, obj_in)


@router.get("/{search_id}", response_model=SearchIndexOut)
def read_search_index(search_id: int, db: Session = Depends(get_db)):
    obj = crud_search.get_search_index(db, search_id)
    if not obj:
        return error_response(404, "SearchEntryNotFound", f"Search entry with id {search_id} not found.")
    return obj
 
@router.get("/", response_model=List[SearchIndexOut])
def list_search_indices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_search.get_all_search_indices(db, skip, limit)
 
@router.get("/search/", response_model=List[SearchIndexOut])
def search_entries(query: str, db: Session = Depends(get_db)):
    return crud_search.search_by_name(db, query)
 
@router.delete("/{search_id}")
def delete_search_index(search_id: int, db: Session = Depends(get_db)):
    obj = crud_search.get_search_index(db, search_id)
    if not obj:
        return error_response(404, "SearchEntryNotFound", f"Cannot delete: search entry with id {search_id} was not found.")   
    crud_search.delete_search_index(db, obj)
   
    return {"message": f"Search entry with ID {search_id} deleted successfully."}