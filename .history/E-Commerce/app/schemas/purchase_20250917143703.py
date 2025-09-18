from pydantic import BaseModel


class PurchaseBase(BaseModel):
    supplier_id: int
    product_id: int
    quantity: int
    unit_cost: float
    payment_status: str = "Pending"


class PurchaseCreate(PurchaseBase):
    pass


class Purchase(PurchaseBase):
    id: int
    total_amount: float

    class Config:
        orm_mode = True
