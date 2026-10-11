from pipeline.enrichment import (
    enrich_transactions_with_client_attributes,
    find_transactions_without_client,
)
from pipeline.exploration import (
    display_labeled_value,
    display_physical_plan,
    display_row_count_change,
    display_sample,
    display_schema,
)
from pipeline.preparation import load_clean_clientes, load_clean_transacciones
from pipeline.spark_session import create_spark_session

ENRICHED_DATASET_NAME = "transacciones_enriquecidas"


def main() -> None:
    spark = create_spark_session()
    try:
        clientes_df = load_clean_clientes(spark)
        transacciones_df = load_clean_transacciones(spark)
        enriched_df = enrich_transactions_with_client_attributes(transacciones_df, clientes_df)

        display_labeled_value(
            ENRICHED_DATASET_NAME,
            "Transacciones sin cliente asociado",
            find_transactions_without_client(transacciones_df, clientes_df).count(),
        )
        display_row_count_change(
            ENRICHED_DATASET_NAME, transacciones_df.count(), enriched_df.count()
        )
        display_schema(enriched_df, ENRICHED_DATASET_NAME)
        display_sample(enriched_df, ENRICHED_DATASET_NAME)
        display_physical_plan(enriched_df, ENRICHED_DATASET_NAME)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
