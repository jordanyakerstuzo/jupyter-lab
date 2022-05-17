from pyspark.sql import SparkSession
from pyspark.sql.column import Column, _to_java_column
from pyspark.sql.types import _parse_datatype_json_string

def from_xml(xml_column, schema, options={}):
    """Parses a given column containing XML data using a supplied schema.
    
    Arguments:
    xml_column (Column): The column to parse.
    schema (StructType): The schema for the column.
    options (dict[str, Any]): A collection of options for the processing of the column."""
    
    spark = SparkSession.getActiveSession()
    if spark is None:
        raise RuntimeError("SparkSession is not currently running.")

    java_column = _to_java_column(xml_column.cast('string'))
    java_schema = spark._jsparkSession.parseDataType(schema.json())
    scala_map = spark._jvm.org.apache.spark.api.python.PythonUtils.toScalaMap(options)
    jc = spark._jvm.com.databricks.spark.xml.functions.from_xml(
        java_column, java_schema, scala_map)
    
    return Column(jc)

def schema_of_xml(df, options={}):
    """Function for retrieving the XML schema of a DataFrame.
    
    Arguments:
    df (DataFrame): The DataFrame to process.
    options (dict[str, Any]): A collection of options for the processing of the DataFrame.
    """
    
    spark = SparkSession.getActiveSession()
    if spark is None:
        raise RuntimeError("SparkSession is not currently running.")

    assert len(df.columns) == 1

    scala_options = spark._jvm.PythonUtils.toScalaMap(options)
    java_xml_module = getattr(getattr(
        spark._jvm.com.databricks.spark.xml, "package$"), "MODULE$")
    java_schema = java_xml_module.schema_of_xml_df(df._jdf, scala_options)
    
    return _parse_datatype_json_string(java_schema.json())