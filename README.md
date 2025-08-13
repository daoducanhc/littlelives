# Ageing Fact Daily ETL

This project builds and updates an **Ageing Fact Table** in MySQL based on invoices, credit notes, and payments data.  
The process runs daily, recalculating outstanding amounts and ageing buckets for all unpaid documents.

---

## Overview

The pipeline:

1. **Extracts** data from three source tables:
   - `invoices`
   - `credit_notes`
   - `payments`

2. **Transforms** data:
   - Merges invoices and credit notes into a unified document table.
   - Aggregates payments by document.
   - Calculates outstanding amounts.
   - Allocates amounts into **ageing buckets** based on the difference in days between the document date and the `as_at_date`.

3. **Loads** the results into:
   - `ageing_fact` table in MySQL
   - Daily CSV export for external use

---

## Requirements

- Python 3.9+
- MySQL 8+
- Python packages:
  - `pandas`
  - `SQLAlchemy`

Install dependencies:
```
pip install pandas SQLAlchemy
```
## Reproducing this project

### 1. Initalize the database and create the tables:
```
mysql -u <username> -p < scripts/0_init_tables.up.sql
```

### 2. Install dependencies:
```
pip install -r requirements.txt
```

### 3. Run testcases

```
PYTHONPATH=. pytest
```

### 4. Run the Ageing Fact ETL process:
```
python src/daily_generate_fact.py
```
