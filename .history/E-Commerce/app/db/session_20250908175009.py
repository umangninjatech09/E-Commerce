from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# For demo use SQLite, in production use PostgreSQL/MySQL
DATABASE_URL = "sqlite:///./customers.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # only needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the Base all models must inherit from
Base = declarative_base()
