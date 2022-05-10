# jupyter-lab

This is a quick Docker setup that allows the running of Jupyter notebooks in a managed environment.

To get started with a local environment, simply execute the `run` task that is included in the Makefile.

## Connecting to Databases via StrongDM

The project has been configured not only with a number of example notebooks, but also comes with a library of helper functions that make connecting to any database a simple exercise.  Simply start a Spark session and use the `get_postgres_table` function as shown below:

```
from lib.database import get_postgres_table
from lib.spark import get_spark_session

spark = get_spark_session()
sc = spark.sparkContext

df = get_postgres_table(database="activate_core_production",
                        partition_col="transaction_time_at",
                        port=9037,
                        table="transactions")
```