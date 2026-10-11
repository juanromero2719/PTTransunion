from pyspark.sql import DataFrame, SparkSession

from pipeline import settings
from pipeline.business_metrics import (
    calculate_amount_by_channel_and_month,
    calculate_amount_by_segment,
)
from pipeline.exploration import (
    display_labeled_value,
    display_physical_plan,
    display_result,
)
from pipeline.performance import persisted
from pipeline.preparation import load_enriched_transacciones
from pipeline.spark_session import create_spark_session
from pipeline.storage import (
    list_partition_directories,
    read_parquet,
    write_parquet_as_single_file,
    write_parquet_partitioned_by_year_month,
)

ENRICHED_DATASET_NAME = "transacciones_enriquecidas"
AMOUNT_BY_CHANNEL_AND_MONTH_NAME = "monto_por_canal_mes"


def compute_and_store_results(enriched_df: DataFrame) -> None:
    amount_by_channel_and_month_df = calculate_amount_by_channel_and_month(enriched_df)

    display_labeled_value(
        ENRICHED_DATASET_NAME, "Nivel de persistencia", enriched_df.storageLevel
    )
    display_physical_plan(amount_by_channel_and_month_df, AMOUNT_BY_CHANNEL_AND_MONTH_NAME)

    write_parquet_partitioned_by_year_month(
        enriched_df, settings.ENRICHED_TRANSACTIONS_OUTPUT_PATH
    )
    write_parquet_partitioned_by_year_month(
        amount_by_channel_and_month_df, settings.AMOUNT_BY_CHANNEL_AND_MONTH_OUTPUT_PATH
    )
    write_parquet_as_single_file(
        calculate_amount_by_segment(enriched_df), settings.AMOUNT_BY_SEGMENT_OUTPUT_PATH
    )


def display_stored_results(spark: SparkSession) -> None:
    display_labeled_value(
        ENRICHED_DATASET_NAME,
        "Particiones escritas",
        list_partition_directories(settings.ENRICHED_TRANSACTIONS_OUTPUT_PATH),
    )
    display_result(
        read_parquet(spark, settings.ENRICHED_TRANSACTIONS_OUTPUT_PATH),
        f"[{ENRICHED_DATASET_NAME}] Lectura desde Parquet",
    )


def main() -> None:
    spark = create_spark_session()
    try:
        with persisted(load_enriched_transacciones(spark)) as enriched_df:
            compute_and_store_results(enriched_df)
        display_stored_results(spark)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
