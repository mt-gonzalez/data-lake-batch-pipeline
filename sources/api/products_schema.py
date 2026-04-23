from pydantic import BaseModel

class ProductBase(BaseModel):
    product_name: str
    category: str
    brand: str
    price: float
    rating: float

# class ReviewsResponse(BaseModel):