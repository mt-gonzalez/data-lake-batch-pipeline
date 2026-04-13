import pandas as pd
import numpy as np

df = pd.read_csv("data/ecommerce_dataset/products.csv")

df["is_current"] = True

prob_of_change = 0.2
max_changes = 1

rows = []

for _, row in df.iterrows():
    rows.append(row.to_dict())

    if np.random.rand() < prob_of_change:
        new_row = row.copy()

        if np.random.rand() < 0.8:
            price = row["price"]
            price_update = np.random.normal(loc=0, scale=0.05)
            new_row["price"] = np.round(price * (1 + price_update), 2)
        else:
            delta = np.random.normal(loc=0, scale=0.05)
            new_rating = row["rating"] + delta

            new_rating = np.clip(new_rating, 1, 5)
            
            new_row["rating"] = np.round(new_rating, 2)

        rows[-1]["is_current"] = False

        new_row["is_current"] = True

        rows.append(new_row.to_dict())
        
scd_df = pd.DataFrame(rows)
scd_df.to_csv("data/processed/products_processed.csv", index=False)


