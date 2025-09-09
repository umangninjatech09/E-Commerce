from fastapi import APIRouter
from app.api.v1.endpoints import customer
from app.api.v1.endpoints.customer import router as customer_router


api_router = APIRouter()

# Mount customer endpoints under /customers
api_router.include_router(customer.router, prefix="/customers", tags=["Customers"])
