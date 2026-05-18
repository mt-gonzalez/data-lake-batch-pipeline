import logging
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time
import boto3

load_dotenv()

logger = logging.getLogger("__name__")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

BASE_URL="http://localhost:8000"

def wait_for_api() :
    
    logger.info("[WAIT_FOR_API] start")
    while True:
        logger.info("[WAIT_FOR_API] Waiting...")
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                logger.info("[WAITING_FOR_API] Ready")
                break
        except:
            pass

        time.sleep(2)


def fetch_products(limit=500) :

    all_data = []
    cursor = None
    seen_cursors = set()
    page = 0

    wait_for_api()
    logger.info("API Ready")

    logger.info("[FETCH_PRODUCTS] start...")
    while True :

        page += 1

        if cursor:
            if cursor in seen_cursors:
                logger.error(f"[FETCH PRODUCTS] cursor loop detected: {cursor}")
                raise RuntimeError("Cursor loop detected")
            
            seen_cursors.add(cursor)

        logger.info(f"[FETCH_PRODUCTS] fetching page={page}, cursor={cursor}")

        response = requests.get(f"{BASE_URL}/products",
                                params={"limit": limit, **({"cursor": cursor} if cursor else {})},
                                timeout=30
        )

        if response.status_code != 200 :
            logger.error(
                f"[FETCH_PRODUCTS] API error page={page} status={response.status_code}"
            )
        
        data = response.json()
        batch = data.get("data", [])
        all_data.extend(batch)

        logger.info(
            f"[FETCH_PRODUCTS] page={page} rows_fetched={len(batch)} total_rows={len(all_data)}"
        )

        cursor = data.get("next_cursor")
        if not cursor:
            logger.info(
                f"[FETCH_PRODUCTS] finished pages={page} total_rows={len(all_data)}"
            )
            break

    return all_data

def parse_and_upload_data(products: dict, date_of_ingestion) :
    
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:9000",
        aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD")
    )

    df = pd.DataFrame(products)
    df.to_csv(f"data/products/up_to_{date_of_ingestion}.csv", index=False)
    
    bucket = os.getenv("S3_BRONZE_BUCKET")
    file = f"data/products/up_to_{date_of_ingestion}.csv"

    s3.upload_file(
        file,
        bucket,
        f"raw/products/up_to_{date_of_ingestion}.csv"
    )

if __name__ == "__main__" :

    date_string = "01/02/2024"
    date = pd.to_datetime(date_string)

    products = fetch_products()

    print("fetch")

    parse_and_upload_data(products, date)

    print("Complete")