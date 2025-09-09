from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.endpoints.customer import router as customer_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Service")

# Directly include customer endpoints
app.include_router(customer_router, prefix="/api/v1/customers", tags=["Customers"])
