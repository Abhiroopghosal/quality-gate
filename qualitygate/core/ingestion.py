from pyspark.sql import functions as F
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StructField, StringType

def ingest_csv(path, expected_schema, spark) -> tuple[DataFrame, dict]:
    """
    Reads a CSV with every col- string, compares against the expected schema, cast toward expected types, and records evidence.
    Returns (Canonical_df and evidence)
    """ 
    df = spark.read.option("header", True).csv(path)

    #df.columns-python listof the column name strings in order
    actual_cols = df.columns

    #expected_schema is a dict {col : typle}, it's keys are the expected columns
    missing_col = sorted(set(expected_schema) - set(actual_cols))
    extra_cols = sorted(set(actual_cols) - set(expected_schema))
    present_cols = sorted(set(actual_cols).intersection(set(expected_schema)))

    # cast failure counting 
    cast_failures = {}

    # Assembling evidence
    evidence = {
        "source_format" : "csv",
        "expected_schema" : expected_schema,
        "missing_columns" : missing_col,
        "extra_columns" : extra_cols,
        "cast_failures" : cast_failures
     } 

    return df, evidence