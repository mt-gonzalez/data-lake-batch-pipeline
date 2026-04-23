from sqlalchemy import Column, String, Float, DateTime
from connection import Base  # connection declarative_base()

class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    updated_at = Column(DateTime, primary_key=True)
    
    product_name = Column(String, nullable=False)
    category = Column(String, index=True)
    brand = Column(String, index=True)
    price = Column(Float)
    rating = Column(Float)