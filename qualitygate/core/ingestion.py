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
    """
    While ingestion we are converting everything into a cannonical parquet format
    Parquet -> typed-at-rest. So conversion say csv -> parquet forces a cast(data can silently die)
    cast failure of the code captures the facts during the cast before it is lost. the 
    failed_coercion is the fingerprint of the silent corruption(say salary column had three real text values which were could not become double hence, casted to null) the failed_coercion records 3
    this is written into the evidence.
    An entity "" can be correctly be converted into null but say for entity "twelve thousand" in a double column that is converted to null then value is lost
    So this peice has total_non_empty that measures values that had something to lose
    The schema rule is sectored to METADATA rule that just reads the count and judges. hence this is piece is incurred into this piece such the scan free design survives
    """
    cast_failures = {}
    for col in present_cols:
        target_type = expected_schema[col]

        #not null and not empty after trimming white pieces
        content_cond = F.col(col).isNotNull() & (F.trim(F.col(col)) != "")

        #count of cells that had content
        total_non_empty = df.filter(content_cond).count()

        #cast result for this column
        casted = F.col(col).try_cast(target_type)

        #content bearing before but null after the cast
        failed_cond = content_cond & casted.isNull()
        failed_coercions = df.filter(failed_cond).count()

        cast_failures[col] = {
            "total_non_empty" : total_non_empty,
            "failed_coercions" : failed_coercions
        }  

    # Assembling evidence
    evidence = {
        "source_format" : "csv",
        "expected_schema" : expected_schema,
        "missing_columns" : missing_col,
        "extra_columns" : extra_cols,
        "cast_failures" : cast_failures
     } 

    return df, evidence