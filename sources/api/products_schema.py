from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
class ProductBase(BaseModel):
    product_id: str
    updated_at: datetime
    product_name: str
    category: str
    brand: str
    price: float
    rating: float

class ProductResponse(BaseModel):
    data: List[ProductBase]
    next_cursor: Optional[str]
    
class Config:
        from_attributes = True