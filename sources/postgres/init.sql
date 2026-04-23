CREATE SCHEMA IF NOT EXISTS source;

CREATE TABLE IF NOT EXISTS source.orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    order_date TIMESTAMP,
    order_status TEXT,
    total_amount DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS source.order_items (
    order_item_id TEXT PRIMARY KEY,
    order_id TEXT,
    product_id TEXT,
    user_id TEXT,
    quantity INT,
    item_price DOUBLE PRECISION,
    item_total DOUBLE PRECISION
);