from fastapi import FastAPI
from . import models
from .database import engine
from .routes import orders

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service API")

app.include_router(orders.router)
