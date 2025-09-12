from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

DATABASE_URL = "sqlite:///./E-Commerce.db"  

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()