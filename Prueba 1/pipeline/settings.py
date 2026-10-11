from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CLIENTES_PATH = DATA_DIR / "clientes.csv"
TRANSACCIONES_PATH = DATA_DIR / "transacciones.csv"

OUTPUT_DIR = PROJECT_ROOT / "output"
ENRICHED_TRANSACTIONS_OUTPUT_PATH = OUTPUT_DIR / "transacciones_enriquecidas"
AMOUNT_BY_CHANNEL_AND_MONTH_OUTPUT_PATH = OUTPUT_DIR / "monto_por_canal_mes"
AMOUNT_BY_SEGMENT_OUTPUT_PATH = OUTPUT_DIR / "monto_por_segmento"

APP_NAME = "abc-clientes-transacciones"
SPARK_MASTER = "local[*]"
SHUFFLE_PARTITIONS = 4
SESSION_TIME_ZONE = "America/Bogota"
LOG_LEVEL = "WARN"

CSV_NULL_LITERAL = "null"
SAMPLE_SIZE = 5

YEAR_MONTH_COLUMN = "anio_mes"
YEAR_MONTH_FORMAT = "yyyy-MM"
