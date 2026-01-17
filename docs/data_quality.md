# Data Quality Strategy

Data quality is treated as a **first-class concern** in this project.

Instead of allowing invalid data to silently propagate, the pipeline enforces strict validation rules and blocks downstream processing when quality thresholds are not met.

---

## Quality Enforcement Approach

Data quality checks are applied in the **Silver layer**, followed by an explicit **Data Quality Gate** before Gold processing.

---

## Validation Rules

The following rules are enforced:

- Mandatory fields must not be null:
  - transaction_id
  - transaction_timestamp
  - store_id
  - customer_id
  - product_id

- Business rules:
  - Quantity > 0
  - Unit price > 0
  - Currency must be EUR
  - Channel must be `online` or `store`

- Timestamp must be parsable into a valid datetime format

---

## Rejected Records Handling

Invalid records are:
- Written to a dedicated rejected table
- Tagged with a rejection reason
- Preserved for audit and debugging

**Rejected Table:**
- `silver_transactions_rejected`

---

## Data Quality Gate

Before Gold transformations run:
- Record counts are checked
- Rejected percentage thresholds are evaluated
- Pipeline fails if quality conditions are not met

This ensures that **only trusted data reaches the analytics layer**.

---

## Benefits

- Prevents silent data corruption
- Improves trust in dashboards
- Enables traceability and auditing
- Mirrors real enterprise data governance practices
