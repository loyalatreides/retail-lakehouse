# Architecture Overview

This project implements a **Retail Data Lakehouse** using a layered **Bronze → Silver → Gold** architecture on Databricks, with external orchestration handled by Apache Airflow.

The design follows modern data engineering best practices: separation of concerns, immutable raw data, data quality enforcement, and analytics-ready outputs.

---

## High-Level Design

The system is composed of four main layers:

1. Data Generation
2. Bronze Layer (Raw)
3. Silver Layer (Cleaned & Validated)
4. Gold Layer (Business Aggregations)

Apache Airflow orchestrates the execution order and enforces dependency management.

---

## Bronze Layer

**Purpose:**  
Store raw, immutable transactional data exactly as ingested.

**Key Characteristics:**
- Minimal transformation
- Schema applied but no validation logic
- Stored as Delta tables
- Acts as the system of record

**Example Table:**
- `retail_lakehouse.bronze_transactions`

---

## Silver Layer

**Purpose:**  
Clean, standardize, and validate data before it is used for analytics.

**Key Transformations:**
- Timestamp parsing
- Null checks
- Business rule validation
- Deduplication using window functions
- Separation of valid and rejected records

**Outputs:**
- `silver_transactions_clean`
- `silver_transactions_rejected`

---

## Gold Layer

**Purpose:**  
Provide analytics-ready datasets optimized for BI and reporting.

**Key Characteristics:**
- Aggregated metrics
- Business-friendly schemas
- Optimized for Power BI consumption

**Example Outputs:**
- Revenue by store
- Product performance metrics
- Customer-level summaries

---

## Analytics Layer

Gold tables are consumed directly by **Power BI**, enabling dashboards and business insights without additional transformation logic.
