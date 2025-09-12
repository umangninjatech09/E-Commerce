from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

DATABASE_URL = "sqlite:///./E-Commerce.db"  

Base = declarative_base()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

def init_db():
    from app.models import Product, Inventory, Pricing, Customer, SearchIndex
    Base.metadata.create_all(bind=engine)