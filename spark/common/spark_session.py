from pyspark.sql import SparkSession

def get_spark(config) -> SparkSession:
    
    builder = (
        SparkSession.builder
            .master("local")
            .appName("pipeline")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.ui.showConsoleProgress", "true")
            
            #MinIO S3 config
            .config("spark.hadoop.fs.s3a.endpoint", config.s3_endpoint)
            .config("spark.hadoop.fs.s3a.access.key", config.s3_access_key)
            .config("spark.hadoop.fs.s3a.secret.key", config.s3_secret_key)
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

    )

    return builder.getOrCreate()