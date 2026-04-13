import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

df = pd.read_csv("data/ecommerce_dataset/users.csv")
df["signup_date"] = pd.to_datetime(df["signup_date"])

df["valid_from"] = df["signup_date"]
df["valid_to"] = pd.NaT
df["is_current"] = True

prob_of_change = 0.3
max_changes = 3

rows = []

for _, row in df.iterrows():
    rows.append(row.to_dict())
    
    if np.random.rand() < prob_of_change:
        n_changes = np.random.randint(1, max_changes + 1)
        last_date = row["signup_date"]
        
        for _ in range(n_changes):
            new_row = row.copy()
            
            change_date = last_date + pd.Timedelta(days=np.random.randint(10, 180))
            
            if np.random.rand() < 0.7: #greater prob of changing email
                new_row["email"] = fake.email()
            else:
                new_row["city"] = fake.city()

            rows[-1]["valid_to"] = change_date
            rows[-1]["is_current"] = False
            
            new_row["valid_from"] = change_date
            new_row["valid_to"] = pd.NaT
            new_row["is_current"] = True
            
            rows.append(new_row.to_dict())
            last_date = change_date

scd_df = pd.DataFrame(rows)
scd_df.to_csv("data/processed/users_processed.csv", index=False)