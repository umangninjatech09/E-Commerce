from fastapi.responses import JSONResponse
from order_service.auth import decode_token

async def jwt_middleware(request, call_next):
    """Global JWT middleware for Order Service"""
    public_paths = ["/docs", "/openapi.json", "/redoc"]  # no login here in order_service

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
