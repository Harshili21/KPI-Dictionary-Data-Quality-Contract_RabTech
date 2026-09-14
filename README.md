# RabTech: KPI Dictionary & Data Quality Contract

[![Data Quality](https://img.shields.io/badge/Data_Quality-Contract_Enforced-2ecc71.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook_Executed-orange.svg)](#)
[![Excel](https://img.shields.io/badge/KPI_Dictionary-Excel_XLSX-1f77b4.svg)](#)

This repository contains the complete implementation of **Task 1: KPI Dictionary & Data Quality Contract** for **RabTech Ed-Commerce Operations**.

---

## 📌 Repository Structure

```
├── README.md                                           # Project Overview & Executive Summary
├── KPI Dictionary & Data Quality Contract/
│   ├── data_quality_contract.md                        # Enterprise Data Quality Contract (SLA, Rules, Escalations)
│   ├── data_quality_profiling.ipynb                    # Executable Jupyter Notebook with all test suites & charts
│   ├── kpi_dictionary.xlsx                             # Professional Multi-Tab Excel KPI & Quality Workbook
│   ├── kpi_dictionary.csv                              # Machine-Readable KPI Dictionary
│   ├── retail-orders-raw.csv                           # Original Raw Incoming Transaction Data
│   ├── retail-data-dictionary.csv                      # Initial Column Metadata & Rules
│   ├── retail-orders-clean.csv                         # Cleansed & Certified Silver Layer Orders Data
│   ├── quarantine_records.csv                          # Quarantined Anomalous Records with Error Tags
│   ├── kpi_visualizations.png                          # Executive KPI & Revenue Charts
│   ├── create_kpi_assets.py                            # Automated Script for Excel/CSV Generation
│   ├── build_and_run_notebook.py                       # Notebook Build & Execution Engine
│   └── task1.txt                                       # Task Specification
```

---

## 🎯 1. Defined Enterprise KPIs (10 Key Metrics)

| KPI ID | KPI Name | Domain | Formula | Refresh Cadence | Business Owner | Target Benchmark |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **KPI-001** | **Gross Merchandise Value (GMV)** | Revenue | $\sum(\text{qty} \times \text{unit\_price})$ for non-failed | Daily (06:00 UTC) | VP of Growth | $\ge ₹150,000 / \text{mo}$ |
| **KPI-002** | **Net Realized Revenue** | Revenue | $\sum(\text{qty} \times \text{unit\_price} \times (1 - \frac{\text{disc}}{100}))$ (Paid) | Daily (06:00 UTC) | Head of Finance | $\ge 85\%$ of GMV |
| **KPI-003** | **Gross Order Volume** | Volume | $\text{COUNT(DISTINCT } \text{order\_id})$ | Intraday / Hourly | Product Ops Manager | $\ge 50 \text{ orders/day}$ |
| **KPI-004** | **Net Completed Orders** | Volume | $\text{COUNT(DISTINCT } \text{order\_id}) \text{ (Paid)}$ | Daily (06:00 UTC) | Head of Commercial Ops | $\ge 80\%$ of Gross |
| **KPI-005** | **Payment Success Rate (PSR)** | Operations | $\frac{\text{Paid Orders}}{\text{Total Orders Attempted}} \times 100\%$ | 15-min Intraday | Fintech & Payments Lead | $\ge 85.0\%$ |
| **KPI-006** | **Average Order Value (AOV)** | Commercial | $\frac{\text{Net Realized Revenue}}{\text{Net Completed Orders}}$ | Daily (06:00 UTC) | VP of Growth | $\ge ₹1,200$ |
| **KPI-007** | **Discount Depth Rate** | Commercial | $\frac{\text{Total Discount Concession}}{\text{Gross Revenue}} \times 100\%$ | Weekly | Marketing Director | $\le 12.0\%$ |
| **KPI-008** | **Refund Rate** | CX | $\frac{\text{Refunded Orders}}{\text{Paid + Refunded}} \times 100\%$ | Daily (06:00 UTC) | CX Lead | $\le 5.0\%$ |
| **KPI-009** | **Category Revenue Share** | Product | $\frac{\text{Category Paid Revenue}}{\text{Total Paid Revenue}} \times 100\%$ | Weekly | Head of Product Portfolio | Kits ~35%, Courses ~45%, Mentorship ~20% |
| **KPI-010** | **Segment Monetization Share** | Growth | $\frac{\text{Segment Paid Revenue}}{\text{Total Paid Revenue}} \times 100\%$ | Weekly | VP of Acquisition | Professional $\ge 45\%$ |

---

## 🔍 2. 5 Core Dimensions of Data Quality Profiling

The executable notebook (`data_quality_profiling.ipynb`) profiles and tests the dataset across the 5 pillars:
1. **Completeness:** Identified null city (`RT-1005`), missing `order_date` (`RT-1011`), and missing `discount_pct` (`RT-1003`).
2. **Uniqueness:** Identified duplicate transaction key `RT-1004`.
3. **Validity:**
   - Range violations: Negative quantity `-1` (`RT-1006`), Out-of-bounds discount `105%` (`RT-1007`).
   - Schema violations: String word quantity `'two'` (`RT-1008`).
   - Calendar date violations: Invalid month `2026-13-10` (`RT-1006`).
4. **Consistency:** Normalized unstandardized casing (e.g., `'student'` $\rightarrow$ `'Student'`, `'paid'` $\rightarrow$ `'Paid'`).
5. **Freshness:** Validated order date spans and verified ingestion window timeliness.

---

## 🛡️ 3. Anomaly Quarantine & Clean Data Outputs

All unresolvable / corrupt records were safely quarantined in [`quarantine_records.csv`](KPI%20Dictionary%20%26%20Data%20Quality%20Contract/quarantine_records.csv) with root-cause failure tags:
- `QRN-1001` (`RT-1004`): `DUPLICATE_ORDER_ID` (P0)
- `QRN-1002` (`RT-1006`): `INVALID_CALENDAR_DATE (2026-13-10) | NEGATIVE_OR_ZERO_QUANTITY (-1)` (P1)
- `QRN-1003` (`RT-1007`): `OUT_OF_BOUNDS_DISCOUNT (105.0%)` (P1)
- `QRN-1004` (`RT-1008`): `NON_NUMERIC_QUANTITY (two)` (P1)
- `QRN-1005` (`RT-1011`): `MISSING_DATE` (P0)

The cleaned, normalized silver dataset is published in [`retail-orders-clean.csv`](KPI%20Dictionary%20%26%20Data%20Quality%20Contract/retail-orders-clean.csv).

---

## 📊 4. KPI Performance & Visuals

![KPI Visualizations](KPI%20Dictionary%20%26%20Data%20Quality%20Contract/kpi_visualizations.png)

| Metric | Clean Silver Value | SLA / Target Status |
| :--- | :--- | :--- |
| **Gross Merchandise Value (GMV)** | **₹8,293.00** | Initial Cohort Baseline |
| **Net Realized Revenue** | **₹4,474.35** | ✅ Healthy (No Negative Inflows) |
| **Payment Success Rate (PSR)** | **57.1%** | ⚠️ Investigating Drop-offs |
| **Average Order Value (AOV)** | **₹1,118.59** | 📊 Near Target (₹1,200) |
| **Discount Depth** | **3.8%** | ✅ Controlled (< 12%) |
| **Refund Rate** | **20.0%** | ⚠️ Product Quality Audit Triggered |

---

## 🚀 5. How to Run Locally

```bash
# Clone the repository
git clone https://github.com/Harshili21/KPI-Dictionary-Data-Quality-Contract_RabTech.git
cd "KPI-Dictionary-Data-Quality-Contract_RabTech/KPI Dictionary & Data Quality Contract"

# Run the KPI spreadsheet generator
python create_kpi_assets.py

# Execute the Data Profiling Notebook
python build_and_run_notebook.py
```

---
*Created as part of RabTech Data Quality & Analytics Engineering initiative.*
