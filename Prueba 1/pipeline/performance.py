from contextlib import contextmanager
from typing import Iterator

from pyspark import StorageLevel
from pyspark.sql import DataFrame


@contextmanager
def persisted(
    df: DataFrame, storage_level: StorageLevel = StorageLevel.MEMORY_AND_DISK
) -> Iterator[DataFrame]:
    persisted_df = df.persist(storage_level)
    try:
        yield persisted_df
    finally:
        persisted_df.unpersist()
