from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    photo = Column(String)
    price = Column(Integer)

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    product = relationship("Product")

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    username = Column(String)
    created_at = Column(String)