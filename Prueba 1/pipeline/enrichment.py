from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from pipeline import settings

JOIN_KEY = "id_cliente"

CLIENT_ATTRIBUTES = [JOIN_KEY, "nombre", "segmento"]

ENRICHED_TRANSACTION_COLUMNS = [
    "id_transaccion",
    "fecha",
    settings.YEAR_MONTH_COLUMN,
    JOIN_KEY,
    "nombre",
    "segmento",
    "canal",
    "monto",
]


def enrich_transactions_with_client_attributes(
    transacciones_df: DataFrame, clientes_df: DataFrame
) -> DataFrame:
    client_attributes_df = clientes_df.select(*CLIENT_ATTRIBUTES)
    return (
        transacciones_df
        .join(F.broadcast(client_attributes_df), on=JOIN_KEY, how="left")
        .select(*ENRICHED_TRANSACTION_COLUMNS)
    )


def find_transactions_without_client(
    transacciones_df: DataFrame, clientes_df: DataFrame
) -> DataFrame:
    return transacciones_df.join(clientes_df, on=JOIN_KEY, how="left_anti")
