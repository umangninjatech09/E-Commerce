from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.endpoints.products import router as product_router
from app.api.v1.endpoints.customers import router as customer_router
from app.api.v1.endpoints.pricing import router as pricing_router
from app.api.v1.endpoints.search import router as search_router
from app.api.v1.endpoints.inventory import router as inventory_router
from app.api.v1.endpoints.supplier import router as supplier_router
from app.api.v1.endpoints.purchase import router as purchase_router
from app.api.v1.endpoints.auth import router as auth_router
from app.a

from app.utils.openapi import custom_openapi
from app.utils.middleware import jwt_middleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Product Catalog System")
app.middleware("http")(jwt_middleware)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"]) 
app.include_router(customer_router, prefix="/customers", tags=["Customers"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(pricing_router, prefix="/pricing", tags=["Pricing"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(supplier_router, prefix="/supplier", tags=["Supplier"])
app.include_router(purchase_router, prefix="/purchase", tags=["Purchase"])
app.include_router(search_router, prefix="/search", tags=["Search"])

app.openapi = lambda: custom_openapi(app)