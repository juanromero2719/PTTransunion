from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StructField, StructType


def summarize_column_quality(field: StructField) -> Column:
    value = F.col(field.name)
    return F.struct(
        F.lit(field.name).alias("columna"),
        F.lit(field.dataType.simpleString()).alias("tipo_esperado"),
        F.lit(field.nullable).alias("admite_nulos"),
        F.count_if(value.isNull()).alias("nulos"),
        F.count_if(
            value.isNotNull() & value.try_cast(field.dataType).isNull()
        ).alias("valores_tipo_invalido"),
    )


def build_column_quality_report(raw_df: DataFrame, schema: StructType) -> DataFrame:
    return (
        raw_df
        .select(F.array(*map(summarize_column_quality, schema.fields)).alias("metricas"))
        .select(F.inline("metricas"))
        .withColumn(
            "cumple",
            (F.col("valores_tipo_invalido") == 0)
            & (F.col("admite_nulos") | (F.col("nulos") == 0)),
        )
    )
