from pyspark.sql import DataFrame

from pipeline import settings

SECTION_DIVIDER = "=" * 80


def print_section_title(title: str) -> None:
    print(f"\n{SECTION_DIVIDER}\n{title}\n{SECTION_DIVIDER}")


def display_schema(df: DataFrame, dataset_name: str) -> None:
    print_section_title(f"[{dataset_name}] Esquema")
    df.printSchema()


def display_sample(df: DataFrame, dataset_name: str, size: int = settings.SAMPLE_SIZE) -> None:
    print_section_title(f"[{dataset_name}] Primeros {size} registros")
    df.show(size, truncate=False)


def display_row_count_change(dataset_name: str, rows_before: int, rows_after: int) -> None:
    print_section_title(f"[{dataset_name}] Conteo de registros")
    print(
        f"Antes: {rows_before} | Después: {rows_after} | "
        f"Eliminados: {rows_before - rows_after}"
    )


def display_result(df: DataFrame, title: str) -> None:
    print_section_title(title)
    df.show(truncate=False)


def display_labeled_value(dataset_name: str, label: str, value: object) -> None:
    print_section_title(f"[{dataset_name}] {label}")
    print(value)


def display_physical_plan(df: DataFrame, dataset_name: str) -> None:
    print_section_title(f"[{dataset_name}] Plan físico de ejecución")
    df.explain()


def display_quality_report(report_df: DataFrame, dataset_name: str) -> None:
    print_section_title(f"[{dataset_name}] Validación de nulos y tipos de datos")
    report_df.show(truncate=False)
