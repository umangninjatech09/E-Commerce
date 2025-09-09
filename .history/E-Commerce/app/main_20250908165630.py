from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1 import routes

app = FastAPI(title="Customer Service", version="1.0.0")

# Create all tables (later models will auto-register here)
Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(routes.router)
