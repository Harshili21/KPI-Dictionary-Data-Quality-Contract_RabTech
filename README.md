# 🚀 RabTech Data Engineering & Analytics Portfolio

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Cleaning-darkblue.svg)](#)
[![Data Quality](https://img.shields.io/badge/Data_Quality-Contract_Enforced-2ecc71.svg)](#)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks_Executed-orange.svg)](#)

Enterprise Data Engineering, Quality Contracts, and Preprocessing projects for **RabTech Operations**.

---

## 📂 Project Directory Structure

```
├── README.md                                           # Global Repository Overview
├── .gitignore                                          # Git ignore configuration
│
├── KPI Dictionary & Data Quality Contract/             # Project 1: Data Quality Contract & KPIs
│   ├── data_quality_contract.md                        # Formal SLA contract and escalation matrix
│   ├── data_quality_profiling.ipynb                    # Executed Jupyter profiling notebook (5 DQ Pillars)
│   ├── kpi_dictionary.xlsx                             # Multi-tab formatted Excel workbook
│   ├── kpi_dictionary.csv                              # 10 Production KPIs definition export
│   ├── retail-orders-clean.csv                         # Cleansed Silver layer transaction records
│   ├── quarantine_records.csv                          # Quarantined anomalous transaction logs
│   ├── implementation_note.md                          # Technical report & methodology
│   └── README.md                                       # Project 1 documentation
│
└── Data Ingestion, Cleaning & Preprocessing with Pandas/ # Project 2: 10,000+ Row Data Cleaning
    ├── data_cleaning_and_preprocessing.ipynb           # Executed end-to-end cleaning & feature engineering notebook
    ├── raw_business_dataset.csv                        # Raw messy retail dataset (12,850 rows, 17 cols)
    ├── clean_dataset.csv                               # Certified clean dataset (12,437 rows, 28 cols)
    ├── cleaning_impact_dashboard.png                   # Visual dashboard of sales, profit, and categories
    ├── implementation_note.md                          # Data cleaning & imputation methodology report
    └── README.md                                       # Project 2 documentation
```

---

## 🌟 Summary of Projects

### 1. [KPI Dictionary & Data Quality Contract](./KPI%20Dictionary%20%26%20Data%20Quality%20Contract)
- **Goal:** Translate business objectives into 10 measurable KPIs and enforce a testable Data Quality Contract.
- **Key Deliverables:** 10 Governed KPIs, automated 5-dimension quality checks (Completeness, Uniqueness, Validity, Consistency, Freshness), dual-destination pipeline (Silver + Quarantine), and incident escalation matrix (P0/P1/P2).

### 2. [Data Ingestion, Cleaning & Preprocessing with Pandas](./Data%20Ingestion,%20Cleaning%20%26%20Preprocessing%20with%20Pandas)
- **Goal:** Ingest and clean a messy 12,850+ row multi-category retail dataset.
- **Key Deliverables:** Deduplication, currency & percentage symbol stripping, multi-format date parsing, missing value imputation, IQR outlier winsorization, 11 engineered features (Profit Margins, COGS, Delivery Days, Temporal breaks), and certified `clean_dataset.csv`.
