import httpx
from fastapi import HTTPException
from jose import jwt, JWTError

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def decode_token(token: str) -> dict:
    """Decode JWT token issued by Auth Service"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
# Define your authentication details
AUTH_URL = "http://127.0.0.1:8000/auth/login"

# Get OAuth2 token from authentication service (use secure credentials in real app)
async def get_oauth_token() -> str:
    async with httpx.AsyncClient() as client:
        payload = {
            "username": "admin",  # Replace with secure credentials
            "password": "admin123",  # Replace with secure credentials
        }
        response = await client.post(AUTH_URL, data=payload)

        if response.status_code == 200:
            token_data = response.json()
            return token_data["access_token"]
        else:
            raise HTTPException(status_code=401, detail="Unable to authenticate with services.")
