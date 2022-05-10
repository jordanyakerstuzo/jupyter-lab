from pyspark.sql import SparkSession
from pyspark.sql.functions import max, min

def get_postgres_table(database: str = None, hostname = "host.docker.internal", partition_col: str = None,
              partition_count = 20, port: int = None, table: str = None, user = "postgres"):
    """Retrieve a DataFrame from a PostgreSQL database table via a JDBC connection.
    
    Arguments:
    database (str): name of the database to retrieve the table from.
    host (str): host server to connect to. Default: host.docker.internal
    partition_col (str): column to use for partitioning the query.
    partition_count (int): the number of partitions to use when partitioning a query. Default: 20
    port (int): port on the server to connect to.
    table (str): the name of the table to retrieve.
    username (str): the username to connect to the database with. Default: user.
    """

    if database is None:
        raise ValueError("database is required")
    if hostname is None:
        raise ValueError("hostname is required")
    if port is None:
        raise ValueError("port is required")
    if not isinstance(port, int):
        raise ValueError("port must be an int")
    if table is None:
        raise ValueError("table is required")

    spark = SparkSession.getActiveSession()
    if spark is None:
        raise RuntimeError("SparkSession is not currently running.")

    df = spark.read \
              .format("jdbc") \
              .option("url", f"jdbc:postgresql://{hostname}:{port}/{database}?user={user}") \
              .option("driver", "org.postgresql.Driver") \
              .option("dbtable", table) \
    
    if partition_col:
        row = df.load() \
                .agg(min(partition_col).alias("min_val"),
                     max(partition_col).alias("max_val")) \
                .collect()[0]
        (min_val, max_val) = row

        df = df.option("partitionColumn", partition_col) \
               .option("lowerBound", min_val) \
               .option("upperBound", max_val) \
               .option("numPartitions", partition_count) \
    
    return df.load()