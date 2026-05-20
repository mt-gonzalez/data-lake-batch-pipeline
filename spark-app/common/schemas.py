from pyspark.sql import types as T

users_schema = T.StructType([
    T.StructField("user_id", T.StringType(), False),
    T.StructField("name", T.StringType(), True),
    T.StructField("email", T.StringType(), True),
    T.StructField("gender", T.StringType(), True),
    T.StructField("city", T.StringType(), True),
    T.StructField("signup_date", T.DateType(), True),
    T.StructField("updated_at", T.TimestampType(), False)
])

products_schema = T.StructType([
    T.StructField("product_id", T.StringType(), False),
    T.StructField("updated_at", T.TimestampType(), False),
    T.StructField("product_name", T.StringType, False),
    T.StructField("category", T.StringType, True),
    T.StructField("brand", T.StringType, True),
    T.StructField("price", T.DecimalType(18, 2), False),
    T.StructField("rating", T.DoubleType, True)
])

orders_schema = T.StructType([
    T.StructField("order_id", T.StringType, False),
    T.StructField("user_id", T.StringType, False),
    T.StructField("order_date", T.TimestampType, False),
    T.StructField("order_status", T.StringType, False),
    T.StructField("total_amount", T.DecimalType(18, 2), False)
])

order_items_schema = T.StructType([
    T.StructField("order_item_id", T.StringType, False),
    T.StructField("order_id", T.StringType, False),
    T.StructField("product_id", T.StringType, False),
    T.StructField("user_id", T.StringType, False),
    T.StructField("quantity", T.IntegerType, False),
    T.StructField("item_price", T.DecimalType(18, 2), False),
    T.StructField("item_total", T.DecimalType(18, 2), False)
])