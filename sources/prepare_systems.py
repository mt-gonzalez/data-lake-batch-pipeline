import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text

load_dotenv()
POSTGRES_URL = os.getenv("POSTGRES_URL")
SQLITE_URL = "sqlite:///./catalog.db"


def populate_postgres():
    engine = create_engine(POSTGRES_URL)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE source.order_items"))
        conn.execute(text("TRUNCATE TABLE source.orders"))

    order_items = pd.read_csv("data/processed/order_items_processed.csv")
    orders = pd.read_csv("data/processed/orders_processed.csv")

    order_items.to_sql(
        "order_items",
        engine, 
        schema="source", 
        if_exists="append", 
        index=False
    )
    
    orders.to_sql(
        "orders", 
        engine, 
        schema="source", 
        if_exists="append", 
        index=False
    )

    print("Postgres seeded")


def populate_sqlite():
    engine = create_engine(SQLITE_URL)


    products = pd.read_csv("data/processed/products_processed.csv")

    products.to_sql("products", engine, if_exists="replace", index=False)

    print("SQLite seeded")


if __name__ == "__main__":
    populate_postgres()
    populate_sqlite()