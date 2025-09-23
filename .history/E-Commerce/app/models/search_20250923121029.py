from sqlalchemy import Column, Integer, Float, ForeignKey, select, case
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.session import Base
from app.models.product import Product
from app.models.customer import Customer
from app.models.pricing import Pricing
 
class SearchIndex(Base):
    __tablename__ = "search_index"
 
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True, nullable=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), index=True, nullable=True)
    pricing_id = Column(Integer, ForeignKey("pricing.id"), index=True, nullable=True)
 
    product = relationship("Product", back_populates="search_index")
    customer = relationship("Customer", back_populates="search_index")
    inventory = relationship("Inventory", back_populates="search_index")
    pricing = relationship("Pricing", back_populates="search_index")
 
    # ---------------- Python-level hybrid properties ----------------
    @hybrid_property
    def name(self):
        if self.product:
            return self.product.name
        elif self.customer:
            return self.customer.name
        return None
 
    @hybrid_property
    def description(self):
        if self.product:
            return self.product.description
        return None
 
    @hybrid_property
    def price(self):
        # Python-level: Product price first, then Pricing amount
        if self.product and getattr(self.product, "price", None) is not None:
            return self.product.price
        if self.pricing and getattr(self.pricing, "amount", None) is not None:
            return self.pricing.amount
        return None
 
    # ---------------- SQL-level hybrid expressions ----------------
    @price.expression
    def price(cls):
        return case(
            (
                cls.product_id != None,
                select(Product.price).where(Product.id == cls.product_id).scalar_subquery()
            ),
            (
                cls.pricing_id != None,
                select(Pricing.amount).where(Pricing.id == cls.pricing_id).scalar_subquery()
            ),
            else_=None
        )
 
    @name.expression
    def name(cls):
        return case(
            (cls.product_id != None, select(Product.name).where(Product.id == cls.product_id).scalar_subquery()),
            (cls.customer_id != None, select(Customer.name).where(Customer.id == cls.customer_id).scalar_subquery()),
            else_=None
        )
 
    @description.expression
    def description(cls):
        return select(Product.description).where(Product.id == cls.product_id).scalar_subquery()
 
 