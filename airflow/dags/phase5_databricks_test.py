from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from datetime import datetime

with DAG(
    dag_id="phase5_databricks_test",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["phase5", "databricks"],
) as dag:

    run_databricks = DatabricksSubmitRunOperator(
        task_id="run_databricks_notebook",
        databricks_conn_id="databricks_default",
        json={
            "run_name": "Airflow Test Run",
            "existing_cluster_id": "0112-030815-4t3irlxe",
            "notebook_task": {
                "notebook_path": "/Shared/hello_airflow"
            }
        }
    )

    run_databricks
