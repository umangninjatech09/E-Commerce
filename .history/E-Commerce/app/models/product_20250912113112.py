from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    sku = Column(String, unique=True, index=True)
    category = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    