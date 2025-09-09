# from app.models.product import Product
# from app.schemas.product import ProductCreate, ProductUpdate

# class ProductService:
#     def create_product(self, db, product: ProductCreate):
#         db_product = Product(**product.dict())
#         db.add(db_product)
#         db.commit()
#         db.refresh(db_product)
#         return db_product

#     def update_product(self, db, product_id: int, product: ProductUpdate):
#         db_product = db.query(Product).filter(Product.id == product_id).first()
#         if not db_product:
#             return None
#         for key, value in product.dict(exclude_unset=True).items():
#             setattr(db_product, key, value)
#         db.commit()
#         db.refresh(db_product)
#         return db_product

#     def delete_product(self, db, product_id: int):
#         db_product = db.query(Product).filter(Product.id == product_id).first()
#         if not db_product:
#             return None
#         db.delete(db_product)
#         db.commit()
#         return db_product

#     def list_products(self, db):
#         return db.query(Product).all()

#     def get_product(self, db, product_id: int):
<<<<<<< HEAD
#         return db.query(Product).filter(Product.id == product_id).first()
=======
#         return db.query(Product).filter(Product.id == product_id).first()
>>>>>>> 3a06cbfd81f9b753e0264c1cf3057f42a055b493
