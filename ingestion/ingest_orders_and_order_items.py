import psycopg2
import boto3
import json
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, date
import logging

load_dotenv()

S3_ENDPOINT = os.getenv("S3_ENDPOINT")

DB_CREDS = {
    "host": "localhost",
    "port": "5432",
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

logger = logging.getLogger("__name__")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def extract_orders(conn, start_date: datetime, end_date: datetime) :

    with conn.cursor() as curr:
        curr.execute("""
                    SELECT *
                    FROM source.orders
                    WHERE order_date >= %s
                    AND order_date < %s
            """, (start_date, end_date)
        )
        
        rows = curr.fetchall()
        col_names = [desc[0] for desc in curr.description]

        data = []

        for row in rows :
            record = dict(zip(col_names, row))

            record["order_date"] = record["order_date"].isoformat()

            data.append(record)

        return data



def extract_order_items(conn, start_date: datetime, end_date: datetime) :

    with conn.cursor() as curr:
        curr.execute("""
                     SELECT oi.*
                     FROM source.order_items oi
                     JOIN source.orders o ON o.order_id = oi.order_id
                     WHERE o.order_date >= %s
                        AND o.order_date < %s
            """, (start_date, end_date)
        )

        rows = curr.fetchall()
        col_names = [desc[0] for desc in curr.description]

        data = []

        for row in rows :
            record = dict(zip(col_names, row))

            data.append(record)

        return data



def normalize_date_for_filename(d):
    
    if isinstance(d, (datetime, date)):
        return d.strftime("%Y-%m-%d")
    
    return str(d)

def write_json_file(data, entity, date):

    date_ready = normalize_date_for_filename(date)

    path = f"data/{entity}/{entity}_up_to={date_ready}.jsonl"

    logger.info(f"[WRITE_JSON] path = {path}")

    #os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf_8") as file:
        for record in data:
            file.write(json.dumps(record) + "\n")



def load_records(file, entity: str, ingestion_date) :

    ingestion_date_ready = normalize_date_for_filename(ingestion_date)

    s3 = boto3.client(
            "s3",
            endpoint_url="http://localhost:9000",
            aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
            aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD")
        )

    bucket = os.getenv("S3_BRONZE_BUCKET")

    path = f"raw/{entity}/source=postgres/orders_up_to={ingestion_date_ready}.jsonl"

    logger.info(f"[LOAD_RECORDS] file name: {file}")

    s3.upload_file(
        file,
        bucket,
        path
    )


if __name__ == "__main__" :

    start_date_string = "01-01-2024"
    end_date_string = "01-02-2024"
    start_date = pd.to_datetime(start_date_string).date()
    end_date = pd.to_datetime(end_date_string).date()  # DATE FORMATEA DE NUEVO A YYYY-MM-DD
    logger.info(f"[END_DATE]: {end_date}")


    conn = psycopg2.connect(**DB_CREDS)

    orders_data = extract_orders(conn, start_date, end_date)

    order_items_data = extract_order_items(conn, start_date, end_date)

    write_json_file(
        orders_data,
        "orders",
        end_date
        )

    write_json_file(
        order_items_data,
        "order_items",
        end_date
        )

    orders_file_name = f"data/orders/orders_up_to={end_date}.jsonl"
    order_items_file_name = f"data/order_items/order_items_up_to={end_date}.jsonl"

    logger.info(f"[MAIN] orders_file_name: {orders_file_name}")
    logger.info(f"[MAIN] orders_file_name: {order_items_file_name}")
    load_records(orders_file_name, "orders", end_date)
    load_records(order_items_file_name, "order_items", end_date)