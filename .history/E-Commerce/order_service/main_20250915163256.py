from fastapi import FastAPI
from order_service.database import Base, engine
from order_service.routes import orders

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")

# Include routes
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
