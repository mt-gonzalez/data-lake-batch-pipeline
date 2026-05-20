from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T

def basic_schema_normalization_products(df: DataFrame) -> DataFrame :

    df = df.na.drop(subset=["product_id", "updated_at", "product_name", "price"])
    
    lower_cols = ["product_name", "category", "brand"]
    for col in lower_cols :
        df = df.withColumn(col, F.lower(F.col(col)))

    df = df.withColumn("updated_at", F.col("updated_at").cast(T.TimestampType()))

    return df

def dedup_products(df: DataFrame) -> DataFrame :

    df = df.dropDuplicates(["product_id", "updated_at"])
    df = df.dropDuplicates(["product_id", "price"])

    return df