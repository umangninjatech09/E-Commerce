from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.endpoints.products import router as product_router
from app.api.v1.endpoints.customers import router as customer_router
from app.api.v1.endpoints.pricing import router as pricing_router
from app.api.v1.endpoints.search import router as search_router
from app.api.v1.endpoints.order import router as order_router
from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Product Catalog System")


app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(customer_router, prefix="/customers", tags=["Customers"])
app.include_router(pricing_router, prefix="/pricing", tags=["Pricing"])
app.include_router(search_router, prefix="/search", tags=["Search"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])