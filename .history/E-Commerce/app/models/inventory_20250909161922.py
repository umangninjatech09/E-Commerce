from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)   # comes from product service
    quantity = Column(Integer, default=0)
    location = Column(String, nullable=True)   # optional (warehouse/store)
