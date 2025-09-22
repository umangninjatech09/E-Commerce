from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from app.db.session import Base, engine
from app.api.v1.endpoints.products import router as product_router
from app.api.v1.endpoints.customers import router as customer_router
from app.api.v1.endpoints.pricing import router as pricing_router
from app.api.v1.endpoints.inventory import router as inventory_router
from app.api.v1.endpoints.auth import router as auth_router
from app.utils.auth import decode_token

# ----------------------------
# Database setup
# ----------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------
# OAuth2 scheme (for Swagger UI Authorize button)
# ----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ----------------------------
# FastAPI app initialization
# ----------------------------
app = FastAPI(title="E-Commerce Product Catalog System")

# ----------------------------
# JWT Middleware
# ----------------------------
@app.middleware("http")
async def jwt_middleware(request, call_next):
    """Global middleware to enforce JWT authentication."""
    public_paths = ["/auth/login", "/docs", "/openapi.json", "/redoc"]

    # Allow public endpoints
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    # Extract Authorization header
    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

    # Validate token
    try:
        decode_token(token.replace("Bearer ", ""))
    except Exception:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    return await call_next(request)
from fastapi import FastAPI
from app.db.session import Base, engine

# Import routers
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

# ----------------------------
# Routers
# ----------------------------
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(customer_router, prefix="/customers", tags=["Customers"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(pricing_router, prefix="/pricing", tags=["Pricing"])

# ----------------------------
# Custom OpenAPI schema (forces Swagger to show Authorize button)
# ----------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="E-Commerce Product Catalog System API",
        routes=app.routes,
    )

    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply security globally
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Override OpenAPI generator
app.openapi = custom_openapi
