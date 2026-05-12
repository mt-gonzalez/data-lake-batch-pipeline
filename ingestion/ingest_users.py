import pandas as pd
from pathlib import Path
from datetime import timedelta
import boto3

def get_files_from_to(start_date, end_date):
    files = [Path]
    
    while start_date <= end_date:
        base = Path("sources/crm")
        date_path = (
            f"year={start_date.year}/" \
            f"month={start_date.month:02d}/" \
            f"day={start_date.day:02d}/" \
            "users.csv"
        )
        
        total_path = base / date_path

        if total_path.exists():
            files.append(total_path)

        start_date += timedelta(days=1)

    return files

def read_file(file):
    df = pd.read_csv(file)

    return df

# The idea is that this functions reads the csv file, convert it to parquet in memory
# and then it uploads it to S3, freeing the memory used
def read_and_write(start_date, end_date):

if __name__ == "__main__":
    start_date_string = "01/01/2024"
    end_date_string = "05/01/2024"
    start_date = pd.to_datetime(start_date_string, dayfirst=True)
    end_date = pd.to_datetime(end_date_string, dayfirst=True)

    res = get_files_from_to(start_date, end_date)
    print(res)

