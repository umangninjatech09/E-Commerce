from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.endpoints.products import router as product_router
from app.api.v1.endpoints.customers import router as customer_router
from app.api.v1.endpoints.inventory import router as inventory_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service")

# Register endpoints
app.include_router(product_router, prefix="/products", tags=["Products"])

# Register endpoints
app.include_router(customer_router, prefix="/customers", tags=["Customers"])

app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
