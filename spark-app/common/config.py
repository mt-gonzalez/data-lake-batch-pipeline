import os
from dataclasses import dataclass

@dataclass(frozen=True)  
class Config:
    s3_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    s3_bronze: str
    s3_silver: str
    s3_gold: str

def load_config():
    return Config(
        s3_endpoint=os.getenv("S3_ENDPOINT"),
        s3_access_key=os.getenv("MINIO_ROOT_USER"),
        s3_secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
        s3_bronze=os.getenv("S3_BRONZE_BUCKET"),
        s3_silver=os.getenv("S3_SILVER_BUCKET"),
        s3_gold=os.getenv("S3_GOLD_BUCKET"),
    )
