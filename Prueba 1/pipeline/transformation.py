from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from pipeline import settings


def remove_transactions_without_amount(transacciones_df: DataFrame) -> DataFrame:
    return transacciones_df.filter(F.col("monto").isNotNull())


def add_year_month_column(df: DataFrame, date_column: str) -> DataFrame:
    return df.withColumn(
        settings.YEAR_MONTH_COLUMN,
        F.date_format(F.col(date_column), settings.YEAR_MONTH_FORMAT),
    )


