from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

# Create DB
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Order Service")

@app.post("/orders/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    return crud.create_order(db, order)

@app.get("/orders/{order_id}", response_model=schemas.OrderOut)
def read_order(order_id: int, db: Session = Depends(database.get_db)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.get("/orders/", response_model=list[schemas.OrderOut])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)

@app.put("/orders/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(database.get_db)):
    updated_order = crud.update_order_status(db, order_id, order_update.status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@app.delete("/orders/{order_id}", response_model=schemas.OrderOut)
def delete_order(order_id: int, db: Session = Depends(database.get_db)):
    deleted_order = crud.delete_order(db, order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted_order
