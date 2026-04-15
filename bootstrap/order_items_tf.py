#This scripts updates the prices of those products which change over time its rating or price
import numpy as np
import pandas as pd

orders_df = pd.read_csv("data/ecommerce_dataset/orders.csv").sort_values("order_date")
products_df = pd.read_csv("data/processed/products_processed.csv").sort_values("updated_at")
order_items_df = pd.read_csv("data/ecommerce_dataset/order_items.csv")

products_df['updated_at'] = pd.to_datetime(products_df['updated_at'])
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])

order_items_expanded = order_items_df.merge(
    orders_df[['order_id', 'order_date']],
    on='order_id',
    how='left'
)

order_items_expanded = order_items_expanded.sort_values(
    ['order_date', 'order_id']
).reset_index(drop=True)


# ----------------------------------------------------------------
# This order_items_processed will be the order_items final version
order_items_processed = pd.merge_asof(
    order_items_expanded,
    products_df,
    left_on="order_date",
    right_on="updated_at",
    by="product_id",
    direction="backward"
)

order_items_processed['item_price'] = order_items_processed['price']
order_items_processed['item_total'] = (order_items_processed['item_price'] * order_items_processed['quantity']).round(2)
order_items_processed = order_items_processed.drop(columns=['order_date', 'product_name',
                                                              'category', 'brand', 'price',
                                                              'rating', 'updated_at'])
# ----------------------------------------------------------------

#-----------------------------------------------------------------
# With the order_items_processed now I update the total_amount column in the orders table
order_total_amounts = order_items_processed.groupby('order_id').agg(
    new_total_amount=('item_total', 'sum')
).round(2).reset_index()

orders_processed = orders_df.merge(
    order_total_amounts,
    how='left',
    on='order_id'
)

orders_processed['total_amount'] = orders_processed['new_total_amount']
orders_processed = orders_processed.drop(columns='new_total_amount')
#-----------------------------------------------------------------

order_items_processed.to_csv("data/processed/order_items_processed.csv", index=False)
orders_processed.to_csv('data/processed/orders_processed.csv', index=False)