from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from pipeline import settings

TOTAL_AMOUNT_COLUMN = "monto_total"
AVERAGE_AMOUNT_COLUMN = "monto_promedio"
TRANSACTION_COUNT_COLUMN = "cantidad_transacciones"
AMOUNT_DECIMALS = 2


def calculate_amount_by_segment(enriched_df: DataFrame) -> DataFrame:
    return (
        enriched_df
        .groupBy("segmento")
        .agg(
            F.sum("monto").alias(TOTAL_AMOUNT_COLUMN),
            F.round(F.avg("monto"), AMOUNT_DECIMALS).alias(AVERAGE_AMOUNT_COLUMN),
            F.count("id_transaccion").alias(TRANSACTION_COUNT_COLUMN),
        )
        .orderBy(F.desc(TOTAL_AMOUNT_COLUMN), "segmento")
    )


def calculate_amount_by_channel_and_month(enriched_df: DataFrame) -> DataFrame:
    return (
        enriched_df
        .groupBy("canal", settings.YEAR_MONTH_COLUMN)
        .agg(
            F.sum("monto").alias(TOTAL_AMOUNT_COLUMN),
            F.count("id_transaccion").alias(TRANSACTION_COUNT_COLUMN),
        )
        .orderBy(F.desc(TOTAL_AMOUNT_COLUMN), "canal", settings.YEAR_MONTH_COLUMN)
    )
