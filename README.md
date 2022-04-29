# jupyter-lab

This is a quick Docker setup that allows the running of Jupyter notebooks in a managed environment.

To get started with a local environment, simply run the `up` task that is included in the Makefile.

## Connecting to Databases via StrongDM

As mentioned in the [Docker Documentation](https://docs.docker.com/desktop/mac/networking/#i-want-to-connect-from-a-container-to-a-service-on-the-host), in order to connect to a host, you simply need to specify `host.docker.internal` and the port as shown below:

```
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("OpenCommerce") \
    .config("spark.jars", "/ext/lib/postgresql-42.3.4.jar") \
    .getOrCreate()

df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://host.docker.internal:9037/activate_rule_production?user=postgres") \
    .option("driver", "org.postgresql.Driver") \
    .option("dbtable", "actions") \
    .load()
```