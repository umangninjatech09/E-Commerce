from fastapi import FastAPI
from db.session import Base, engine
from app.api import routes

app = FastAPI(title="Customer Service", version="1.0.0")

# Create tables in SQLite
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(routes.router)
