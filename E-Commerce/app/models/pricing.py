from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.product import Product

class Pricing(Base):
    __tablename__ = "pricing"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    currency = Column(String, default="USD")
    amount = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)

    product = relationship("Product", back_populates="pricings")
