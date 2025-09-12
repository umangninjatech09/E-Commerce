from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from app.db.session import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)   # Link to Customer Service
    product_id = Column(Integer, index=True)    # Link to Product Service
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
