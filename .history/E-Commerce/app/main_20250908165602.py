from fastapi import FastAPI
# from db.session import Base, engine
from app.api.v1 import routes

app = FastAPI(title="Customer Service", version="1.0.0")

# Create DB tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(routes.router)
