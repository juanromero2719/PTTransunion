from typing import Callable

from pyspark.sql import DataFrame, SparkSession

from pipeline.catalog import CLIENTES, TRANSACCIONES, DatasetSource
from pipeline.exploration import display_row_count_change, display_sample, display_schema
from pipeline.ingestion import load_raw_dataset
from pipeline.preparation import prepare_clientes, prepare_transacciones
from pipeline.spark_session import create_spark_session


def clean_and_display(
    spark: SparkSession,
    source: DatasetSource,
    prepare: Callable[[DataFrame], DataFrame],
) -> DataFrame:
    raw_df = load_raw_dataset(spark, source)
    clean_df = prepare(raw_df)

    display_row_count_change(source.name, raw_df.count(), clean_df.count())
    display_schema(clean_df, source.name)
    display_sample(clean_df, source.name)
    return clean_df


def main() -> None:
    spark = create_spark_session()
    try:
        clean_and_display(spark, CLIENTES, prepare_clientes)
        clean_and_display(spark, TRANSACCIONES, prepare_transacciones)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
