from fastapi import FastAPI, Depends, Query

from sqlalchemy import select
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy.orm import Session

from typing import List, Optional

from connection import get_db
from products_model import Product
from products_schema import ProductResponse

from datetime import datetime

app = FastAPI(title="Products Catalog API", debug=True)

def build_cursor(product):
    return f"{product.updated_at.isoformat()}|{product.product_id}"

def parse_cursor(cursor: str):
    updated_at_str, product_id = cursor.split("|")
    return datetime.fromisoformat(updated_at_str), product_id

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products", response_model=ProductResponse)
def get_product(
    db: Session = Depends(get_db),
    limit: int = Query(100, le=1000),
    cursor: Optional[str] = None
):
    stmt = select(Product).order_by(Product.updated_at.asc(), Product.product_id.asc()).limit(limit)

    if cursor:
        last_update, last_product = parse_cursor(cursor)

        stmt = stmt.where(
            or_(
                Product.updated_at > last_update,
                and_(Product.updated_at == last_update,
                     Product.product_id > last_product
                )
            )
        )

    results = db.scalars(stmt).all()

    next_cursor = build_cursor(results[-1]) if results else None

    return {"data" : results,
            "next_cursor" : next_cursor}