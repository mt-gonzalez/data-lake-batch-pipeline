import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

df = pd.read_csv("data/ecommerce_dataset/users.csv")
df["signup_date"] = pd.to_datetime(df["signup_date"])

df["updated_at"] = df["signup_date"]

prob_of_change = 0.4
max_changes = 4

rows = []

for _, row in df.iterrows():
    rows.append(row.to_dict())
    
    if np.random.rand() < prob_of_change:
        new_row = row.copy()
        n_changes = np.random.choice(
            [1, 2, 3, 4],
            p=[0.6, 0.25, 0.1, 0.05]
        )
        
        last_date = row["updated_at"]
        email = row["email"]
        city = row["city"]
        
        for _ in range(n_changes):
            change_date = last_date + pd.Timedelta(
                days=np.random.randint(10, 180),
                seconds=np.random.randint(0, 86400),
                microseconds=np.random.randint(0, 1_000_000)
            )
            
            if np.random.rand() < 0.9: #greater prob of changing email
                email = fake.email()
                new_row["email"] = email
            else:
                city = fake.city()
                new_row["city"] = city
            
            last_date = change_date
            new_row["updated_at"] = change_date
            rows.append(new_row.to_dict())

scd_df = pd.DataFrame(rows)
scd_df.to_csv("data/processed/users_processed.csv", index=False, date_format="%Y-%m-%dT%H:%M:%S.%f")