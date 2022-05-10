import os

from typing import Dict, List

from pyspark import SparkConf
from pyspark.sql import SparkSession

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"

SESSION_DEFAULT_CONF = {
    "spark.sql.adaptive.advisoryPartitionSizeInBytes": "128m",
    "spark.sql.adaptive.coalescePartitions.minPartitionSize": "2",
    "spark.sql.adaptive.coalescePartitions.initialPartitionNum": "2",
    "spark.sql.adaptive.coalescePartitions.enabled": "true"
}

SPARK_DEFAULT_PACKAGES = [
    "org.postgresql:postgresql:42.3.5"
]

def get_spark_session(config: Dict[str, str] = None, driver = "spark://driver:7077",
                      name = "OpenCommerce", packages: List[str] = None):
    """Helper function to initialize a SparkSession object.

    Arguments:
    config (dict): a collection of configuration options to be passed to the Spark session.
    driver (str): the name of the driver to connect the session with. Default: spark://driver:7077.
    name (str): the name of the Spark application.
    packages (list): a collection of packages to install within the Spark application.
    """
    conf = {**SESSION_DEFAULT_CONF, **config} if config else {**SESSION_DEFAULT_CONF}
    
    if packages:
        pkgs = list({*SPARK_DEFAULT_PACKAGES, *packages})
    else:
        pkgs = list([*SPARK_DEFAULT_PACKAGES])
    conf["spark.jars.packages"] = ",".join(pkgs)

    builder = SparkSession.builder \
                          .master(driver) \
                          .appName(name)

    for k, v in conf.items():
        builder = builder.config(k, v)
    
    return builder.getOrCreate()