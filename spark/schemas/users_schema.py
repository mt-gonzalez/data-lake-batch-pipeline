from pyspark.sql import types as T

users_schema = T.StructType([
    T.StructField("user_id", T.StringType(), False),
    T.StructField("name", T.StringType(), True),
    T.StructField("email", T.StringType(), True),
    T.StructType("gender", T.StringType(), True),
    T.StructType("city", T.StringType(), True),
    T.StructType("signup_date", T.DateType(), True),
    T.StructType("updated_at", T.TimestampType(), False)
])
