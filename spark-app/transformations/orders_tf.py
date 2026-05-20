from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T

def basic_schema_normalization_orders(df: DataFrame) -> DataFrame :

    df = df.withColumn("order_date", F.col("order_date").cast(T.TimestampType()))
    df = df.withColumn("order_status", F.lower(F.trim(F.col("order_status"))))

    df = df.na.drop(how="any")

    return df

def dedup_orders(df: DataFrame) -> DataFrame :

    df = df.dropDuplicates(["order_id", "order_status"])

