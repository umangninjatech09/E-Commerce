from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierOut
from app.crud import supplier as crud_supplier
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=SupplierOut)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    return crud_supplier.create_supplier(db, supplier)
    
@router.get("/", response_model=Page[SupplierOut])
def read_suppliers(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    query = db.query(SupplierModel)  # ✅ ORM model
    return paginate(query, page, size)

@router.get("/{supplier_id}", response_model=SupplierOut)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = crud_supplier.get_supplier(db, supplier_id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.put("/{supplier_id}", response_model=SupplierOut)
def update_supplier(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    db_supplier = crud_supplier.update_supplier(db, supplier_id, supplier)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.delete("/{supplier_id}", response_model=SupplierOut)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = crud_supplier.delete_supplier(db, supplier_id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier
