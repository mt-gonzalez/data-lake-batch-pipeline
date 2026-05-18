from sqlalchemy import Column, Integer, String, Float, DateTime
from connection import Base  # connection declarative_base()

class Product(Base):
    __tablename__ = "products"

    row_id = Column(Integer, primary_key=True)
    updated_at = Column(DateTime, primary_key=True)
    product_id = Column(String, primary_key=False)
    product_name = Column(String, nullable=False)
    category = Column(String, index=True)
    brand = Column(String, index=True)
    price = Column(Float)
    rating = Column(Float)