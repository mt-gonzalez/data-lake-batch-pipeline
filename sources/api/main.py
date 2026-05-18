from fastapi import FastAPI, Depends, Query

from sqlalchemy import select
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy.orm import Session

from typing import List, Optional

from connection import get_db
from products_model import Product
from products_schema import ProductResponse
import logging

from datetime import datetime

logger = logging.getLogger("__name__")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

app = FastAPI(title="Products Catalog API", debug=True)

def build_cursor(product):
    return f"{product.updated_at.isoformat()}|{product.row_id}"

def parse_cursor(cursor: str):
    updated_at_str, row_id = cursor.split("|")
    return (
        datetime.fromisoformat(updated_at_str), 
        int(row_id)
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products", response_model=ProductResponse)
def get_product(
    db: Session = Depends(get_db),
    limit: int = Query(100, le=1000),
    cursor: Optional[str] = None
):
    try:

        stmt = select(Product)
        stmt = stmt.order_by(Product.updated_at.asc(), Product.row_id.asc())
        stmt = stmt.limit(limit + 1)

        if cursor:
            last_update, last_row = parse_cursor(cursor)

            stmt = stmt.where(
                Product.row_id > last_row
            )

        results = db.scalars(stmt).all()

        has_next = len(results) > limit

        items = results[:limit]

        next_cursor = build_cursor(items[-1]) if has_next and items else None

        logger.info(f"[FETCH PRODUCTS] cursor loop detected cursor={cursor}, next_cursor={next_cursor}")

        return {"data" : items,
                "next_cursor" : next_cursor}
    
    except Exception as e:
        print("ERROR:", e)
        raise