from fastapi import APIRouter



api_router = APIRouter()

# Mount customer endpoints under /customers
api_router.include_router(customer.router, prefix="/customers", tags=["Customers"])
