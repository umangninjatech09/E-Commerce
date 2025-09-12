from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, confirmed, shipped, delivered
    created_at = Column(DateTime(timezone=True), server_default=func.now())
