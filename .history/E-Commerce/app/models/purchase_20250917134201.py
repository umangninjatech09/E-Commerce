from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Purchase(Base):
    __tablename__ = "purchases