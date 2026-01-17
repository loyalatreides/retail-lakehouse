# Orchestration Design

This project uses **Apache Airflow** for external orchestration instead of notebook chaining.

This design choice improves reliability, observability, and operational control.

---

## Why Airflow?

Airflow provides:
- Explicit task dependencies
- Retry and failure handling
- Centralized monitoring
- Decoupling of compute and orchestration

---

## DAG Structure

The main DAG orchestrates the pipeline in the following order:

1. Bronze ingestion
2. Silver transformations
3. Data Quality Gate
4. Gold aggregations

Each task triggers a Databricks notebook using the Databricks provider.

---

## Execution Characteristics

- `max_active_runs = 1` to avoid overlapping executions
- Manual triggering for controlled runs
- Idempotent notebook logic to support safe reruns

---

## Failure Handling

If any task fails:
- Downstream tasks do not execute
- Errors are visible in the Airflow UI
- Data quality failures stop the pipeline before Gold processing

---

## Production Alignment

This orchestration pattern mirrors real-world data platforms where:
- Compute is isolated
- Orchestration is centralized
- Pipelines are observable and auditable
