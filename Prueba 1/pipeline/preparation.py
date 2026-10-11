from pyspark.sql import DataFrame, SparkSession

from pipeline.catalog import CLIENTES, TRANSACCIONES
from pipeline.enrichment import enrich_transactions_with_client_attributes
from pipeline.ingestion import cast_to_schema, load_raw_dataset
from pipeline.transformation import (
    add_year_month_column,
    remove_transactions_without_amount,
)


def prepare_clientes(raw_clientes_df: DataFrame) -> DataFrame:
    clientes_df = cast_to_schema(raw_clientes_df, CLIENTES.schema)
    return add_year_month_column(clientes_df, "fecha_alta")


def prepare_transacciones(raw_transacciones_df: DataFrame) -> DataFrame:
    transacciones_df = cast_to_schema(raw_transacciones_df, TRANSACCIONES.schema)
    transacciones_with_amount_df = remove_transactions_without_amount(transacciones_df)
    return add_year_month_column(transacciones_with_amount_df, "fecha")


def load_clean_clientes(spark: SparkSession) -> DataFrame:
    return prepare_clientes(load_raw_dataset(spark, CLIENTES))


def load_clean_transacciones(spark: SparkSession) -> DataFrame:
    return prepare_transacciones(load_raw_dataset(spark, TRANSACCIONES))


def load_enriched_transacciones(spark: SparkSession) -> DataFrame:
    return enrich_transactions_with_client_attributes(
        load_clean_transacciones(spark), load_clean_clientes(spark)
    )
