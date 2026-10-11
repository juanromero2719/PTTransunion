from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from pipeline import settings


def write_parquet_partitioned_by_year_month(df: DataFrame, path: Path) -> None:
    (
        df.repartition(settings.YEAR_MONTH_COLUMN)
        .write
        .mode("overwrite")
        .partitionBy(settings.YEAR_MONTH_COLUMN)
        .parquet(str(path))
    )


def write_parquet_as_single_file(df: DataFrame, path: Path) -> None:
    df.coalesce(1).write.mode("overwrite").parquet(str(path))


def read_parquet(spark: SparkSession, path: Path) -> DataFrame:
    return spark.read.parquet(str(path))


def list_partition_directories(path: Path) -> list[str]:
    return sorted(child.name for child in path.iterdir() if child.is_dir())
