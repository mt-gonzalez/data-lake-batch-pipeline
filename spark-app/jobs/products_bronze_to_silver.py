from common.config import load_config
from common.spark_session import get_spark
from common.schemas import products_schema
from transformations import products_tf, scd2_tf

config = load_config

spark = get_spark()

bronze_path = f"s3a://{config.s3_bronze}/raw/products/source=sqlite_catalog/"
silver_path = f"s3a://{config.s3_silver}/staged/products"

df = spark.read.csv(bronze_path, schema=products_schema)

df = products_tf.basic_schema_normalization_products(df)
df = products_tf.dedup_products(df)
df = scd2_tf.build_scd2(df, "product_id")

df.write.mode("overwrite").parquet(silver_path)

df.show(100)
