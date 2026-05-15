from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T 

def basic_schema_normalization(df: DataFrame) -> DataFrame :

    df = df.na.drop(["user_id", "updated_at"])
    df = df.withColumn("email", F.lower(F.col("email")))
    df = df.withColumn("signup_date", F.col("signup_date").cast(T.DateType()))
    df = df.withColumn("updated_at", F.col("updated_at").cast(T.TimestampType()))
    
    return df


def dedup_users(df: DataFrame) -> DataFrame :
    
    return (
        df.dropDuplicates(["user_id", "updated_at"])
    )