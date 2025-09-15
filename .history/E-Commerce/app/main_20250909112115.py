from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.endpoints.customers import router as customer_router


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Service")

# Register endpoints
app.include_router(customer_router, prefix="/customers", tags=["Customers"])
