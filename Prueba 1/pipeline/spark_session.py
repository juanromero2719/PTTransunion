from pyspark.sql import SparkSession

from pipeline import settings


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName(settings.APP_NAME)
        .master(settings.SPARK_MASTER)
        .config("spark.sql.shuffle.partitions", settings.SHUFFLE_PARTITIONS)
        .config("spark.sql.session.timeZone", settings.SESSION_TIME_ZONE)
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.ansi.enabled", "true")
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel(settings.LOG_LEVEL)
    return spark
