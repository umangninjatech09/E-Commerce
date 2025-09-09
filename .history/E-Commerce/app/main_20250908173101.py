from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.routes import api_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Service")

# Include all API v1 routes
app.include_router(api_router, prefix="/api/v1")
