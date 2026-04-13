import pandas as pd
import numpy as np

df = pd.read_csv("data/ecommerce_dataset/products.csv")
orders_df = pd.read_csv("data/ecommerce_dataset/orders.csv")
orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

min_date = orders_df["order_date"].min()
max_date = orders_df["order_date"].max()

df["updated_at"] = min_date

prob_of_change = 0.3
max_changes = 2

rows = []

for _, row in df.iterrows():
    rows.append(row.to_dict())

    if np.random.rand() < prob_of_change:
        new_row = row.copy()
        n_changes = np.random.randint(1, max_changes + 1)

        price = row["price"]
        rating = row["rating"]
        last_date = row["updated_at"]
        
        for _ in range(n_changes):
            change_date = last_date + pd.Timedelta(
                days=np.random.randint(5, 60),
                seconds=np.random.randint(0, 86400),
                microseconds=np.random.randint(0, 1_000_000))

            if np.random.rand() < 0.7:
                price_update = np.random.normal(0, 0.05)
                price = np.round(price * (1 + price_update), 2)  # 🔑 update directo
                new_row["price"] = price
            else:
                delta = np.random.normal(0, 0.05)
                rating = np.round(np.clip(rating + delta, 1, 5), 2)  # 🔑 update directo
                new_row["rating"] = rating

            last_date = change_date
            new_row["updated_at"] = change_date
            rows.append(new_row.to_dict())
        
scd_df = pd.DataFrame(rows)
scd_df.to_csv("data/processed/products_processed.csv", index=False, date_format="%Y-%m-%dT%H:%M:%S.%f")


