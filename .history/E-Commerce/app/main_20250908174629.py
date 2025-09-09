from fastapi import FastAPI
from app.db.session import Base, engine


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Service")

# Directly include customer endpoints
app.include_router(customer_router, prefix="/api/v1/customers", tags=["Customers"])
