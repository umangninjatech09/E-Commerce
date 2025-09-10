import httpx

PRICING_SERVICE_URL = "http://localhost:8002/pricing"

async def get_price(product_id: int) -> float:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PRICING_SERVICE_URL}/{product_id}")
        resp.raise_for_status()
        return resp.json().get("price")
