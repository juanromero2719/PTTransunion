from dataclasses import dataclass
from pathlib import Path

from pyspark.sql.types import (
    DateType,
    DecimalType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

from pipeline import settings


@dataclass(frozen=True)
class DatasetSource:
    name: str
    path: Path
    schema: StructType


CLIENTES = DatasetSource(
    name="clientes",
    path=settings.CLIENTES_PATH,
    schema=StructType([
        StructField("id_cliente", IntegerType(), nullable=False),
        StructField("nombre", StringType(), nullable=False),
        StructField("segmento", StringType(), nullable=False),
        StructField("fecha_alta", DateType(), nullable=False),
    ]),
)

TRANSACCIONES = DatasetSource(
    name="transacciones",
    path=settings.TRANSACCIONES_PATH,
    schema=StructType([
        StructField("id_transaccion", LongType(), nullable=False),
        StructField("id_cliente", IntegerType(), nullable=False),
        StructField("fecha", DateType(), nullable=False),
        StructField("monto", DecimalType(18, 2), nullable=False),
        StructField("canal", StringType(), nullable=False),
    ]),
)
