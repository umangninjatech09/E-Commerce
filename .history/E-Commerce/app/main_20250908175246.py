from fastapi import FastAPI
from app.api.v1.endpoints.customers import router as customer_router
from app.db.session import engine
from db.base_class import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Service")

# Directly include customer endpoints
app.include_router(customer_router, prefix="/api/v1/customers", tags=["Customers"])


from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
