from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    """Customize OpenAPI schema to always show JWT Authorize button."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="E-Commerce Product Catalog System API",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


from fastapi.responses import JSONResponse
from app.utils.auth import decode_token

async def jwt_middleware(request, call_next):
    """Global JWT middleware for protected routes."""
    public_paths = ["/auth/login", "/docs", "/openapi.json", "/redoc", "/customers/{customer_id}"]

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
