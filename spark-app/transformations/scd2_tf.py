from pyspark.sql import DataFrame, Column, Window
from pyspark.sql import functions as F
from pyspark.sql import types as T

def build_scd2(df: DataFrame, id_column: str) -> DataFrame :
    w = Window.partitionBy(id_column).orderBy("updated_at")

    df = df.withColumn("valid_from", F.col("updated_at"))
    df = df.withColumn(
        "valid_to",
        F.lead("updated_at").over(w)
    )
    df = df.withColumn(
        "current",
        F.when(F.col("valid_to").isNull(), True).otherwise(False)
    )
    
    return df