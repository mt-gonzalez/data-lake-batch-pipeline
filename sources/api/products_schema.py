from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
class ProductBaseInternal(BaseModel):
    row_id: int
    product_id: str
    updated_at: datetime
    product_name: str
    category: str
    brand: str
    price: float
    rating: float

class ProductResponseItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str
    updated_at: datetime
    product_name: str
    category: str
    brand: str
    price: float
    rating: float
    
class ProductResponse(BaseModel):
    data: List[ProductResponseItem]
    next_cursor: Optional[str]
    
class Config:
        from_attributes = True