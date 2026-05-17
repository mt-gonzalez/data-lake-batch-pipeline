from common.config import load_config
from common.spark_session import get_spark
from common.schemas import users_schema
from transformations import users_tf, scd2_tf

config = load_config()

spark = get_spark(config)
 
bronze_path = f"s3a://{config.s3_bronze}/raw/users/"
silver_path = f"s3a://{config.s3_silver}/staged/users"

df = spark.read.csv(bronze_path, schema=users_schema)

df = users_tf.basic_schema_normalization(df)
df = users_tf.dedup_users(df)
df = scd2_tf.build_scd2(df, "user_id")


df.write.mode("overwrite").parquet(silver_path)

df.show(100)