from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator


# ---------
# Variables
# ---------
EXISTING_CLUSTER_ID = Variable.get("DATABRICKS_EXISTING_CLUSTER_ID")

NB_BRONZE = Variable.get("NB_BRONZE_PATH")
NB_SILVER = Variable.get("NB_SILVER_PATH")
NB_GOLD = Variable.get("NB_GOLD_PATH")
NB_DQ_GATE = Variable.get("NB_DQ_GATE_PATH")



def submit_notebook(*, task_id: str, notebook_path: str, base_parameters: dict) -> DatabricksSubmitRunOperator:
    return DatabricksSubmitRunOperator(
        task_id=task_id,
        databricks_conn_id="databricks_default",
        json={
            "run_name": f"retail_lakehouse__{task_id}",
            "existing_cluster_id": EXISTING_CLUSTER_ID,
            "timeout_seconds": 60 * 60,
            "notebook_task": {
                "notebook_path": notebook_path,
                "base_parameters": base_parameters,
            },
            "tags": {
                "project": "retail_lakehouse",
                "layer": task_id,
                "orchestrator": "airflow",
            },
        },
    )


default_args = {
    "owner": "kamran",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="retail_lakehouse_bronze_silver_gold",
    description="Orchestrate Databricks Bronze → Silver → Gold notebooks (Retail Lakehouse)",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(hours=3),
    tags=["retail", "lakehouse", "databricks", "phase5_2"],
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    common_params = {
        "process_date": "{{ ds }}",
        "run_id": "{{ run_id }}",
        "mode": "incremental",
        "env": "dev",
    }

    with TaskGroup("bsg") as bsg:
        bronze = submit_notebook(
            task_id="bronze",
            notebook_path=NB_BRONZE,
            base_parameters={**common_params, "layer": "bronze"},
        )

        silver = submit_notebook(
            task_id="silver",
            notebook_path=NB_SILVER,
            base_parameters={**common_params, "layer": "silver"},
        )

        dq_gate = submit_notebook(
            task_id="dq_gate",
            notebook_path=NB_DQ_GATE,
            base_parameters={**common_params, "layer": "dq_gate"},
        )

        gold = submit_notebook(
            task_id="gold",
            notebook_path=NB_GOLD,
            base_parameters={**common_params, "layer": "gold"},
        )

        bronze >> silver >> dq_gate >> gold

    start >> bsg >> end
