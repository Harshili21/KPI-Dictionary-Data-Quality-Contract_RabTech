# Implementation Note: KPI Dictionary & Data Quality Contract

**Project:** RabTech Ed-Commerce Operations  
**Deliverable:** Task 1 — Data Quality Engineering & Metric Governance  
**Author:** Data Platform & Analytics Engineering Team  
**Date:** 2026-01-15  
**Status:** Certified & Production-Ready  

---

## 1. Executive Summary

In enterprise commerce and ed-tech operations, downstream business decisions (such as revenue forecasting, discounting strategy, and marketing spend) rely heavily on granular transactional logs. However, raw ingestion pipelines frequently encounter malformed, duplicate, or out-of-bounds records due to upstream client-side bugs, unvalidated API inputs, network retry bursts, and manual entry errors.

This project implements an end-to-end **Data Quality Framework** for RabTech by:
1. Translating ambiguous commercial goals into **10 formally governed KPIs** with clear mathematical formulations, grains, and SQL queries.
2. Building an automated, executable profiling suite covering the **5 core dimensions of data quality** (**Completeness**, **Uniqueness**, **Validity**, **Consistency**, and **Freshness**).
3. Implementing a dual-destination pipeline that routes valid records to a certified Silver table (`retail-orders-clean.csv`) and isolates corrupt rows to an audit-ready Quarantine table (`quarantine_records.csv`).
4. Establishing a binding **Data Quality Contract** (`data_quality_contract.md`) with explicit failure thresholds, incident severity tiers (P0/P1/P2), and automated escalation protocols.

---

## 2. Dataset Context & Anomaly Breakdown

The raw transactional table (`retail-orders-raw.csv`) contains 12 recorded checkout attempts across Learning Kits, Course Access, and Mentor Sessions. Ingestion analysis revealed several critical failure patterns:

| Anomaly Class | Affected Records | Raw Observation | Impact on Downstream Reporting | Quarantine / Remediation Action |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Key Collision (Uniqueness)** | `RT-1004` (Row 5 & 6) | Exact duplicate row for `RT-1004` | Overstates platform GMV and order volume by $100\%$ for that order. | Deduplicated: Ingested first occurrence, routed duplicate to quarantine with `DUPLICATE_ORDER_ID` (P0). |
| **Out-of-Bounds Range (Validity)** | `RT-1007` (Row 9) | `discount_pct = 105%` ($> 100\%$) | Causes negative net revenue line items and distorts revenue reconciliation. | Quarantined with `OUT_OF_BOUNDS_DISCOUNT` (P1); alerted Commercial Ops. |
| **Negative / Unparsable Value (Validity)** | `RT-1006` (Row 8), `RT-1008` (Row 10) | `quantity = -1`, `quantity = 'two'` | Fails mathematical aggregation; negative quantities corrupt inventory & GMV. | Quarantined with `NEGATIVE_OR_ZERO_QUANTITY` and `NON_NUMERIC_QUANTITY` (P1). |
| **Malformed Date / Calendar Error (Validity)** | `RT-1006` (Row 8), `RT-1002` (Row 3) | `2026-13-10` (Month 13), `03/01/2026` (slash format) | Month 13 crashes date-partitioned storage; slash format breaks ISO sorting. | Parsed `03/01/2026` to `2026-01-03`; Quarantined `2026-13-10` with `INVALID_CALENDAR_DATE` (P1). |
| **Missing Critical Keys (Completeness)** | `RT-1011` (Row 13), `RT-1005` (Row 7) | Missing `order_date`, Missing `city` | Missing date prevents time-series cohort assignment; missing city impairs geo-analytics. | Quarantined missing date `RT-1011` (P0); imputed missing city in `RT-1005` to `'Unknown'` (P2). |
| **Categorical Casing (Consistency)** | `RT-1003` (Row 4), `RT-1002` (Row 3) | `student`, `paid` (lowercase) | Creates fragmented aggregation buckets (`Student` vs `student`). | Standardized via automated title-casing transformation in Silver layer (P2). |

---

## 3. Data Architecture & Cleansing Workflow

```
               [ Upstream Ingestion (Webhooks / Checkout API) ]
                                      │
                                      ▼
                   [ Bronze Layer: retail-orders-raw.csv ]
                                      │
                                      ▼
                ┌───────────────────────────────────────────┐
                │   Data Quality Verification Test Engine   │
                │   - Completeness & Schema Assertions      │
                │   - Range, Type & Date Validity Checks    │
                │   - Primary Key Uniqueness Test           │
                └─────────────────────┬─────────────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 │                                         │
        [ 100% Valid / Resolvable ]              [ Fatal Anomalies (P0/P1) ]
                 │                                         │
                 ▼                                         ▼
   [ Silver Layer: retail-orders-clean.csv ]     [ Quarantine: quarantine_records.csv ]
                 │                                         │
                 ▼                                         ▼
   [ Gold Layer: KPI Calculation Marts ]         [ P0/P1 Alerting & JIRA Escalation ]
   - Gross Merchandise Value (GMV)               - On-Call PagerDuty Trigger
   - Net Realized Revenue                        - Root-Cause Remediation Playbook
   - Payment Success Rate (PSR)
   - Average Order Value (AOV)
```

---

## 4. KPI Definition & Measurement Matrix

10 production KPIs were defined across Revenue, Volume, Operations, Product, and Customer Strategy:

| KPI ID | KPI Name | Mathematical Formula | Grain | Target SLA | Business Decision Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KPI-001** | **Gross Merchandise Value (GMV)** | $\sum(\text{quantity} \times \text{unit\_price})$ for non-failed orders | Daily | $\ge ₹150,000 / \text{mo}$ | VP of Growth & Commercial Ops |
| **KPI-002** | **Net Realized Revenue** | $\sum(\text{quantity} \times \text{unit\_price} \times (1 - \frac{\text{discount\_pct}}{100}))$ for Paid | Daily | $\ge 85\%$ of GMV | Head of Finance |
| **KPI-003** | **Gross Order Volume** | $\text{COUNT(DISTINCT } \text{order\_id})$ | Hourly | $\ge 50 \text{ orders/day}$ | Product Operations Manager |
| **KPI-004** | **Net Completed Orders** | $\text{COUNT(DISTINCT } \text{order\_id}) \text{ WHERE payment\_status = 'Paid'}$ | Daily | $\ge 80\%$ of Gross | Head of Commercial Ops |
| **KPI-005** | **Payment Success Rate (PSR)** | $\frac{\text{Count of Paid Orders}}{\text{Total Orders Attempted}} \times 100\%$ | 15-min | $\ge 85.0\%$ | Fintech & Payments Lead |
| **KPI-006** | **Average Order Value (AOV)** | $\frac{\text{Net Realized Revenue}}{\text{Net Completed Orders}}$ | Daily | $\ge ₹1,200$ | VP of Growth & Commercial Ops |
| **KPI-007** | **Discount Depth Rate** | $\frac{\text{Total Discount Concession Amount}}{\text{Gross Value of Discounted Orders}} \times 100\%$ | Weekly | $\le 12.0\%$ | Marketing & Growth Director |
| **KPI-008** | **Refund Rate** | $\frac{\text{Count of Refunded Orders}}{\text{Count of Paid + Refunded Orders}} \times 100\%$ | Monthly | $\le 5.0\%$ | Customer Experience Lead |
| **KPI-009** | **Category Revenue Share** | $\frac{\text{Category Net Revenue}}{\text{Total Net Revenue}} \times 100\%$ | Monthly | Kits ~35%, Courses ~45%, Mentorship ~20% | Head of Product Portfolio |
| **KPI-010** | **Segment Monetization Share** | $\frac{\text{Cohort Net Revenue}}{\text{Total Net Revenue}} \times 100\%$ | Monthly | Professional $\ge 45\%$ | VP of Acquisition |

---

## 5. Quantitative Impact: Dirty Data vs. Cleaned Data

Calculating business metrics directly on unvalidated raw data produces significant distortion:

| Metric | Computed on Raw (Unvalidated) | Computed on Cleaned (Silver Layer) | Distortion & Risk Identified |
| :--- | :--- | :--- | :--- |
| **Gross Merchandise Value (GMV)** | ₹11,388.00 | **₹8,293.00** | **+37.3% False Inflation** caused by duplicate `RT-1004` and unparsable orders. |
| **Net Realized Revenue** | Distorted (Negative row: $-₹99.90$) | **₹4,474.35** | `105%` discount created invalid negative revenue line items. |
| **Order Count (Gross)** | 12 rows | **7 valid orders** | **5 corrupt records** (duplicate, invalid month, string quantity, missing date). |
| **Payment Success Rate** | 58.3% | **57.1%** | Distorted denominator due to duplicate checkout events. |

---

## 6. Operational Governance & Escalation Playbook

1. **P0 Incidents (Critical / Blocking):**
   - *Triggers:* Duplicate `order_id`, missing `order_date` $> 5\%$ of batch, schema drop.
   - *SLA:* Ack in 15 mins, Fix in 2 hours.
   - *Action:* Pipeline halted; downstream reporting tables protected; on-call engineer paged.
2. **P1 Incidents (High Quality Breach):**
   - *Triggers:* Quantity $\le 0$, `discount_pct` $> 100\%$, Payment Success Rate $< 75\%$.
   - *SLA:* Ack in 1 hour, Fix in 6 hours.
   - *Action:* Records quarantined into `quarantine_records.csv`; automated incident ticket dispatched to upstream API team.
3. **P2 Incidents (Minor Consistency / Schema Evolution):**
   - *Triggers:* Casing mismatch (`student` vs `Student`), non-critical nulls (`city`).
   - *SLA:* Ack in 4 hours, Fix in 24 hours.
   - *Action:* Automated normalization applied in Silver layer; weekly review board updated.

---

## 7. Recommendations for Engineering Roadmap

1. **Shift-Left Validation:** Embed JSON Schema / Pydantic validation directly in the upstream Checkout API to reject negative quantities, non-numeric strings, and discounts $> 100\%$ at request time.
2. **Idempotency Keys:** Enforce idempotency keys on payment webhook endpoints to eliminate primary key duplications at the gateway layer.
3. **Automated CI/CD Checks:** Incorporate `Great Expectations` or `dbt test` suites in CI/CD pipelines to validate schema migrations before production release.
