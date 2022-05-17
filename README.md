# jupyter-lab

This is a quick Docker setup that allows the running of Jupyter notebooks in a managed environment.

## Running Jupyter

### Jupyter Server
The Docker Compose configuration file within this repository contains all of the services necessary to run a fully self-contained instance of Jupyter server.  To launch the server, simply run `make run:jupyter` and then open your browser to `http://localhost:8888`. Once the Jupyter environment has loaded, you're ready to run an existing notebook or create your own.

### Jupyter with VS Code
[Jupyter with VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) allows the same flexibility of using Jupyter server but with the ease and convenience of utilizing the VS Code interface and shortcuts.

#### **Prerequisites**

* Docker
* Python 3.9
* [Python extensions for VS Code](https://github.com/Microsoft/vscode-python)
* Open JDK 11
     * Ensure that system-wide linking is complete.
* `host.docker.internal` mapped to `127.0.0.1`
* Packages from `requirements.txt` installed

#### **Running**

1. Launch the Spark services within docker by running `make run`.
1. Select an existing notebook or create a new notebook.
1. Select the Python 3.9 kernel by clicking the "Select Kernel" button in the top toolbar of the notebook.
1. Write and/or run your code.

#### **Notes**

* When creating a new session within VS Code you will need to specify the driver host as follows:
    ```python
    from lib.spark import get_spark_session

    spark = get_spark_session("spark://localhost:7077")
    sc = spark.sparkContext
    ```

## Connecting to Databases via StrongDM

The project has been configured not only with a number of example notebooks, but also comes with a library of helper functions that make connecting to any database a simple exercise.  Simply start a Spark session and use the `get_postgres_table` function as shown below:

```python
from lib.database import get_postgres_table
from lib.spark import get_spark_session

spark = get_spark_session()
sc = spark.sparkContext

df = get_postgres_table(database="activate_core_production",
                        partition_col="transaction_time_at",
                        port=9037,
                        table="transactions")
```

## Connecting to S3 via Leapp

The Docker Compose services and the Spark sessions have been configured to seamlessly integrate with your AWS credentials file (i.e., `~/.aws/credentials`) in order to authenticate to S3. Because of this, all session credentials created via Leapp will be accessible within your local Spark envirnment allowing you to connect to any number of AWS environments.

**NOTE:** when connecting to a new environment or renewing your existing credentials, it may be necessary to restart your Jupyter Kernel to detect the new credentials.