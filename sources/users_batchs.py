import pandas as pd
import os

df = pd.read_csv("data/processed/users_processed.csv")

df["updated_at"] = pd.to_datetime(df["updated_at"])

df["date"] = df["updated_at"].dt.date

output_dir = "sources/users_snapshots"
os.makedirs(output_dir, exist_ok=True)

for date, group in df.groupby("date"):
    file_path = f"{output_dir}/users_{date}.csv"
    group.to_csv(file_path, index=False)

print("Daily users records created")