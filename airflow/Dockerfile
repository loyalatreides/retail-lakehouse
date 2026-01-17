ARG AIRFLOW_VERSION=2.9.3
FROM apache/airflow:${AIRFLOW_VERSION}

ARG AIRFLOW_VERSION=2.9.3
ARG PYTHON_VERSION=3.12

USER airflow

# Let Airflow constraints decide the compatible provider version
RUN pip install --no-cache-dir \
  apache-airflow-providers-databricks \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
