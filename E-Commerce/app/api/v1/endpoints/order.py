from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderOut
from app.crud import order as crud
from app.db.session import get_db
from app.services.product_service import check_stock
from app.services.pricing_service import get_price

router = APIRouter()

@router.post("/", response_model=OrderOut)
async def place_order(data: OrderCreate, db: Session = Depends(get_db)):
    validated_items = []
    total_amount = 0.0

    for item in data.items:
        stock_ok = await check_stock(item.product_id, item.qty)
        if not stock_ok:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {item.product_id}")

        price = await get_price(item.product_id)
        line_total = price * item.qty
        total_amount += line_total

        validated_items.append({
            "product_id": item.product_id,
            "qty": item.qty,
            "price": price
        })

    order = crud.create_order(db, data, validated_items, total_amount)
    return order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.cancel_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
