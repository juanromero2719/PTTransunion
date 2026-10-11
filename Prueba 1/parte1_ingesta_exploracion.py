from pyspark.sql import DataFrame, SparkSession

from pipeline.catalog import CLIENTES, TRANSACCIONES, DatasetSource
from pipeline.data_quality import build_column_quality_report
from pipeline.exploration import display_quality_report, display_sample, display_schema
from pipeline.ingestion import cast_to_schema, load_raw_dataset
from pipeline.spark_session import create_spark_session


def ingest_and_explore(spark: SparkSession, source: DatasetSource) -> DataFrame:
    raw_df = load_raw_dataset(spark, source)
    typed_df = cast_to_schema(raw_df, source.schema)

    display_schema(typed_df, source.name)
    display_sample(typed_df, source.name)
    display_quality_report(build_column_quality_report(raw_df, source.schema), source.name)
    return typed_df


def main() -> None:
    spark = create_spark_session()
    try:
        ingest_and_explore(spark, CLIENTES)
        ingest_and_explore(spark, TRANSACCIONES)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
