from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def basic_schema_normalization_oi(df: DataFrame) -> DataFrame :
    
    df = df.na.drop(how="any")

    df = df.filter(
        F.col("quantity") * F.col("item_price") == F.col("item_total")
    )

    return df

def dedup_oi(df: DataFrame) -> DataFrame :

    df.dropDuplicates(["order_item_id"])

    return df