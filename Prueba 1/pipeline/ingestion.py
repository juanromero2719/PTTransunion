from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType

from pipeline import settings
from pipeline.catalog import DatasetSource


class MissingColumnsError(ValueError):
    pass


def read_csv_as_strings(spark: SparkSession, source: DatasetSource) -> DataFrame:
    return (
        spark.read
        .option("header", True)
        .option("inferSchema", False)
        .option("nullValue", settings.CSV_NULL_LITERAL)
        .csv(str(source.path))
    )


def ensure_expected_columns_are_present(raw_df: DataFrame, schema: StructType) -> None:
    missing_columns = set(schema.fieldNames()) - set(raw_df.columns)
    if missing_columns:
        raise MissingColumnsError(f"Columnas faltantes: {sorted(missing_columns)}")


def load_raw_dataset(spark: SparkSession, source: DatasetSource) -> DataFrame:
    raw_df = read_csv_as_strings(spark, source)
    ensure_expected_columns_are_present(raw_df, source.schema)
    return raw_df


def cast_to_schema(raw_df: DataFrame, schema: StructType) -> DataFrame:
    return raw_df.select([
        F.col(field.name).try_cast(field.dataType).alias(field.name)
        for field in schema.fields
    ])
