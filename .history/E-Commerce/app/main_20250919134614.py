from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.endpoints.products import router as product_router
from app.api.v1.endpoints.customers import router as customer_router
from app.api.v1.endpoints.pricing import router as pricing_router
from app.api.v1.endpoints.inventory import router as inventory_router
from app.api.v1.endpoints.auth import router as auth_router

# Import custom OpenAPI + middleware
from app.utils.openapi import custom_openapi
from app.utils.middleware import jwt_middleware

# ----------------------------
# Database setup
# ----------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------
# FastAPI app initialization
# ----------------------------
app = FastAPI(title="E-Commerce Product Catalog System")

# ----------------------------
# Middleware
# ----------------------------
app.middleware("http")(jwt_middleware)

# ----------------------------
# Routers
# ----------------------------
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(customer_router, prefix="/customers", tags=["Customers"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(pricing_router, prefix="/pricing", tags=["Pricing"])

# ----------------------------
# Custom OpenAPI schema
# ----------------------------
app.openapi = lambda: custom_openapi(app)
