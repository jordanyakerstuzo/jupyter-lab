from pyspark.sql import DataFrame
from pyspark.sql.functions import col

def add_col_prefix(df: DataFrame, prefix: str):
    cols = (col(c).alias(f"{prefix}_{c}") for c in df.columns)
    return df.select(*cols)