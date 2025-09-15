from fastapi import APIRouter

router = APIRouter()

from app.api.v1.endpoints import customers
