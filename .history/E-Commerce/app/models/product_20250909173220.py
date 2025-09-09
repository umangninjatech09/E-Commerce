from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base  # Make sure your Base comes from your database setup
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=True)

    inventory = relationship("Inventory", back_populates="product", uselist=False)