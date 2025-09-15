from fastapi import APIRouter
from app.api.\v1.endpoints import customer


api_router = APIRouter()

# Mount customer endpoints under /customers
api_router.include_router(customer.router, prefix="/customers", tags=["Customers"])
