import pandas as pd
import os

df = pd.read_csv("data/processed/users_processed.csv")

df["updated_at"] = pd.to_datetime(df["updated_at"])

df["year"] = df["updated_at"].dt.year
df["month"] = df["updated_at"].dt.month
df["day"] = df["updated_at"].dt.day

base_output_dir = "sources/crm"

for (year, month, day), group in df.groupby(["year", "month", "day"]):
    
    partition_path = (
        f"{base_output_dir}/"
        f"year={year}/month={month:02d}/day={day:02d}"
    )
    
    os.makedirs(partition_path, exist_ok=True)
    
    file_path = f"{partition_path}/users.csv"
    
    group.to_csv(file_path, index=False)

print("Users records partitioned by year/month/day")