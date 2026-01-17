# 🏗️ Retail Lakehouse Project  
**Databricks • Apache Airflow • Delta Lake • Power BI**

---

## 📌 Project Overview

This project implements a **production-grade Retail Data Lakehouse** using **Databricks**, **Apache Airflow**, **Delta Lake**, and **Power BI**, following a **Bronze → Silver → Gold** architecture with an automated **Data Quality (DQ) Gate**.

The solution demonstrates how raw transactional data can be ingested, validated, orchestrated, audited, and transformed into **trusted, analytics-ready datasets**, closely mirroring real-world enterprise data platforms.

---

## 🎯 Key Objectives

- Build a scalable **Lakehouse architecture**
- Separate raw, clean, and business-ready data layers
- Enforce **data quality checks before analytics**
- Orchestrate pipelines using **Apache Airflow**
- Enable **safe reruns, observability, and failure handling**
- Deliver **Power BI–ready Gold datasets**

---

## 🧱 Technology Stack

- **Databricks** – Data processing & Delta Lake storage  
- **Apache Airflow (Dockerized)** – External orchestration  
- **Delta Lake** – ACID-compliant storage layers  
- **Power BI** – Analytics and visualization  
- **Python / PySpark** – Transformations and data quality logic  

---

## 🏛️ High-Level Architecture

```text
Synthetic Retail Data
(Generated Transactions)
        ↓
Bronze Layer
Raw Delta Tables
(Immutable Ingestion)
        ↓
Silver Layer
Cleaned & Validated Data
(Deduplication, Parsing)
        ↓
Data Quality Gate
Validation Rules
(Fail / Pass Thresholds)
        ↓
Gold Layer
Business Aggregations
(BI-Optimized Tables)
        ↓
Power BI Dashboards
Reporting & Insights
```

---

## 📂 Repository Structure (Overview)

```text
retail-lakehouse/
├── airflow/
│   ├── dags/               → Airflow DAGs
│   ├── Dockerfile          → Airflow image
│   └── docker-compose.yml  → Local orchestration
├── notebooks/
│   ├── bronze/             → Raw ingestion
│   ├── silver/             → Cleaning & DQ
│   └── gold/               → Aggregations
├── data_generator/         → Synthetic data scripts
├── data/                   → Sample/reference data
├── docs/                   → Architecture & DQ docs
├── powerbi/                → Local dashboards
├── README.md
└── .gitignore
```

---

## 🚀 Key Features

Bronze–Silver–Gold Lakehouse architecture

External orchestration using Apache Airflow

Explicit Data Quality Gate before Gold layer

Idempotent, rerunnable pipelines

Power BI–ready analytics datasets

---

## 📊 Analytics Layer

The Gold layer outputs are designed to be directly consumed by **Power BI**, enabling:
- Revenue trends
- Store and product performance
- Customer-level insights
- Channel analysis

  ---

## 📊 Power BI Dashboards

The Gold-layer datasets produced by the lakehouse are consumed directly by **Power BI** to enable business reporting and analytics.

### Dashboard Highlights

#### Overview Dashboard
![Overview Dashboard](powerbi/screenshots/Executive_Overview.png)

#### Revenue by Store
![Revenue by Store](powerbi/screenshots/Product_Performance.png)

#### Product Performance
![Product Performance](powerbi/screenshots/Store_Performance.png)

> Power BI `.pbix` files are intentionally excluded from version control.  
> Screenshots are provided for demonstration purposes.

---

## 🧪 How to Run Locally (Airflow Orchestration)

This project runs **Apache Airflow locally via Docker Compose** to orchestrate Databricks notebooks (**Bronze → Silver → DQ Gate → Gold**).

---

### ✅ Prerequisites

- **Docker Desktop** installed and running
- A **Databricks workspace** + an existing cluster (or job cluster setup in the DAG)
- A **Databricks Personal Access Token (PAT)**
- Databricks notebooks available in Workspace (paths configured in the DAG)

---

### 1️⃣ Clone the repository

git clone https://github.com/████████/retail-lakehouse.git
cd retail-lakehouse

### 2️⃣ Configure environment variables (local only)
Create/update this file:
airflow/.env

Add your Databricks details:
#### Databricks workspace host (NO https://)
DATABRICKS_HOST=adb-████████████████.██.azuredatabricks.net

#### Databricks Personal Access Token
DATABRICKS_TOKEN=████████████████████████████████

#### Cluster ID (if your DAG uses an existing cluster)
DATABRICKS_CLUSTER_ID=████████████████
🔒 Security note: .env is intentionally excluded from version control via .gitignore.

### 3️⃣ Start Airflow (Docker Compose)
From the repo root:
cd airflow
docker compose up -d
Airflow UI will be available at:

http://localhost:8080

### 4️⃣ Login to Airflow
Use the credentials defined by your Airflow Docker setup.
(Common default for the official Airflow docker-compose is:)

Username: airflow

Password: airflow

(If your setup differs, check airflow/docker-compose.yaml.)

### 5️⃣ Trigger the DAG
In Airflow UI:

Go to DAGs

Enable: retail_lakehouse_bronze_silver_gold

Click ▶ Trigger DAG

Monitor execution in Grid / Graph view and per-task logs.

### 6️⃣ Stop Airflow (when finished)

docker compose down
Optional: remove volumes for a clean reset:

docker compose down -v
🧭 Databricks Notebook Paths (Configured in DAG)
Update the DAG or variables to match your Databricks Workspace paths:

Bronze: /Workspace/Users/████████/retail-lakehouse/02_bronze_ingestion

Silver: /Workspace/Users/████████/retail-lakehouse/03_silver_cleaning

Gold: /Workspace/Users/████████/retail-lakehouse/04_gold_aggregations

✅ Expected Outcome
After a successful run:

Bronze Delta tables are created/refreshed

Silver clean + rejected tables are produced

DQ gate validates data health (if enabled)

Gold aggregations are refreshed and ready for Power BI

---

## 🧠 Why This Project Matters

This project goes beyond simple ETL by demonstrating:
- Real-world **data governance practices**
- External orchestration instead of notebook chaining
- Production-style **quality enforcement**
- End-to-end ownership from ingestion to BI

---

## 📌 Notes

- Secrets and environment variables are excluded via `.gitignore`
- Airflow logs and Power BI binaries are kept local only
- Detailed architecture and DQ logic can be found in `/docs`

---

## 👤 Author

**Kamran Habib**  
Data Analytics & Data Engineering Projects 
