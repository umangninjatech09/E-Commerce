# import httpx

# PRODUCT_SERVICE_URL = "http://localhost:8001/products"

# async def check_stock(product_id: int, qty: int) -> bool:
#     async with httpx.AsyncClient() as client:
#         resp = await client.get(f"{PRODUCT_SERVICE_URL}/{product_id}/stock")
#         resp.raise_for_status()
#         stock = resp.json().get("stock", 0)
#         return stock >= qty



import httpx
from fastapi import HTTPException

PRODUCT_SERVICE_URL = "http://localhost:8000/products"
# PRODUCT_SERVICE_URL = "http://product-service:8000/products"
# PRODUCT_SERVICE_URL = "http://127.0.0.1:8000/products"  # Matches product service


async def check_stock(product_id: int, qty: int):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{PRODUCT_SERVICE_URL}/{product_id}/stock")
            resp.raise_for_status()
            data = resp.json()
            return data["stock"] >= qty
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Product service unavailable: {str(e)}")