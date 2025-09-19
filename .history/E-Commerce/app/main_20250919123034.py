from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.db.session import Base, engine
from app.api.v1.endpoints.products import router as product_router
from app.api.v1.endpoints.customers import router as customer_router
from app.api.v1.endpoints.pricing import router as pricing_router
from app.api.v1.endpoints.inventory import router as inventory_router
from app.api.v1.endpoints.auth import router as auth_router
from app.utils.auth import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce Product Catalog System",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": "swagger-ui",
    },
)
# ✅ Global JWT middleware
@app.middleware("http")
async def jwt_middleware(request, call_next):
    # allow login + docs + openapi.json + redoc without token
    public_paths = ["/auth/login", "/docs", "/openapi.json", "/redoc"]
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

    try:
        decode_token(token.replace("Bearer ", ""))
    except Exception:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    return await call_next(request)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(customer_router, prefix="/customers", tags=["Customers"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(pricing_router, prefix="/pricing", tags=["Pricing"])
