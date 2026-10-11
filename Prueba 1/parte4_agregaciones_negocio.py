from pipeline.business_metrics import (
    calculate_amount_by_channel_and_month,
    calculate_amount_by_segment,
)
from pipeline.exploration import display_result
from pipeline.preparation import load_enriched_transacciones
from pipeline.spark_session import create_spark_session


def main() -> None:
    spark = create_spark_session()
    try:
        enriched_df = load_enriched_transacciones(spark)

        display_result(
            calculate_amount_by_segment(enriched_df),
            "Monto total y promedio por segmento",
        )
        display_result(
            calculate_amount_by_channel_and_month(enriched_df),
            "Monto total por canal y mes",
        )
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
