from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import httpx

# Auth service public values
SECRET_KEY = "your_secret_key"   # must match auth service
ALGORITHM = "HS256"

# Tells Swagger to use token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ✅ Verify JWT token from incoming requests
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload  # return decoded token data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
