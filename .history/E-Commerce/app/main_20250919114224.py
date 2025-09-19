from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.endpoints.products import router as product_router
from app.api.v1.endpoints.customers import router as customer_router
from app.api.v1.endpoints.pricing import router as pricing_router
from app.api.v1.endpoints.inventory import router as inventory_router
from app.api.v1.endpoints.auth import router as auth_router
from app.utils.auth import decode_token

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Product Catalog System")

# ✅ Global JWT middleware
@app.middleware("http")
async def jwt_middleware(request, call_next):
    # allow login endpoint without token
    if request.url.path.startswith("/auth/login"):
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

    try:
        decode_token(token.replace("Bearer ", ""))
    except Exception:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    return await call_next(request)

app.include_router(customer_router, prefix="/customers", tags=["Customers"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(pricing_router, prefix="/pricing", tags=["Pricing"])
