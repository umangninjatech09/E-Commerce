from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base

class SearchIndex(Base):
    __tablename__ = "search_index"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    price = Column(Float)
    stock_status = Column(String)
    rating = Column(Float)