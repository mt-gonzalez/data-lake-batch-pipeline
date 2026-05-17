import pandas as pd
from pathlib import Path
from datetime import timedelta
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

def get_files_from_to(start_date, end_date):
    files = []
    
    while start_date < end_date:
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

# The idea is that this functions reads the csv file and then it uploads it to S3, freeing the memory used
def read_and_write(files):
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:9000",
        aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD")
    )

    for file in files:
        parts = file.parts
        year = parts[2].replace("year=", "")
        month = parts[3].replace("month=", "")
        day = parts[4].replace("day=", "")

        s3_tag = f"users/year={year}/month={month}/day={day}"
        file_name = f"users_{year}{month}{day}.csv"

        to_upload = str(file)

        s3.upload_file(
            to_upload,
            "datalake-bronze",
            f"raw/{s3_tag}/{file_name}"
        )
    

if __name__ == "__main__":
    start_date_string = "01/02/2024"    # Managed by Airflow
    end_date_string = "01/03/2024"
    start_date = pd.to_datetime(start_date_string, dayfirst=True)
    end_date = pd.to_datetime(end_date_string, dayfirst=True)

    #res = get_files_from_to(start_date, end_date)

    files = get_files_from_to(start_date, end_date)

    read_and_write(files)

    print("Complete")

