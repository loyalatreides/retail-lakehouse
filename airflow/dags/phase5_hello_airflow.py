from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# This function is the actual "work"
def hello_airflow():
    print("✅ Airflow is working correctly!")

# DAG definition
with DAG(
    dag_id="phase5_hello_airflow",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["phase5", "learning"],
) as dag:

    hello_task = PythonOperator(
        task_id="hello_airflow_task",
        python_callable=hello_airflow
    )

    hello_task
