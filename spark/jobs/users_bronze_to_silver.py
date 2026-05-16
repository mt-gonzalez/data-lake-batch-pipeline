from common.config import Config
from common.spark_session import get_spark
from schemas.users_schema import users_schema
from transformations import users_tf, scd2_tf

config = Config()
spark = get_spark(config)

bronze_path = f"s3a://{config.s3_bronze}/users/"
silver_path = f"s3a://{config.s3_silver}/users_scd2/"

df = spark.read.schema(users_schema).csv(bronze_path)

df = users_tf.basic_schema_normalization(df)
df = users_tf.dedup_users(df)
df = scd2_tf.build_scd2(df)


df.write.mode("overwrite").parquet(silver_path)