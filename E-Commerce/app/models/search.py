from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class SearchIndex(Base):
    __tablename__ = "search_index"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True, nullable=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), index=True, nullable=True)
    pricing_id = Column(Integer, ForeignKey("pricing.id"), index=True, nullable=True)

    product = relationship("Product", back_populates="search_index")
    customer = relationship("Customer", back_populates="search_index")
    inventory = relationship("Inventory", back_populates="search_index")
    pricing = relationship("Pricing", back_populates="search_index")
