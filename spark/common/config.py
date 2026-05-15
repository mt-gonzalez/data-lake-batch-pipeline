import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    
    env: str = os.getenv("ENV", "local")

    s3_endpoint: str = os.getenv("S3_ENDPOINT")
    s3_access_key: str = os.getenv("MINIO_ROOT_USER")
    s3_secret_key: str = os.getenv("MINIO_ROOT_PASSWORD")
    s3_bronze: str = os.getenv("S3_BRONZE_BUCKET")
    s3_silver: str = os.getenv("S3_SILVER_BUCKET")
    s3_gold: str = os.getenv("S3_GOLD_BUCKET")
