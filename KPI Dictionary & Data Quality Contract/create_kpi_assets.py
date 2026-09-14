import os
import pandas as pd
import xlsxwriter

output_dir = r"c:\Users\Harshili\Desktop\RabTech\Project1"
excel_path = os.path.join(output_dir, "kpi_dictionary.xlsx")
csv_path = os.path.join(output_dir, "kpi_dictionary.csv")

# 1. Define KPI Dictionary Data (10 KPIs)
kpis = [
    {
        "KPI_ID": "KPI-001",
        "KPI_Name": "Gross Merchandise Value (GMV)",
        "Domain": "Revenue",
        "Business_Definition": "Total aggregate value of goods and services purchased by learners prior to discounts, cancellations, and refunds.",
        "Formula": "SUM(quantity * unit_price)",
        "SQL_Expression": "SUM(CASE WHEN payment_status != 'Failed' THEN quantity * unit_price ELSE 0 END)",
        "Grain": "Order Line / Daily / Monthly",
        "Filters_Exclusions": "Exclude failed orders and quarantined records with invalid quantities/prices.",
        "Business_Owner": "VP of Growth & Commercial Ops",
        "Technical_Owner": "Data Engineering Lead",
        "Refresh_Cadence": "Daily (06:00 UTC)",
        "Target_Benchmark": ">= ₹150,000 / month",
        "SLA_Alert_Threshold": "< 80% of 7-day moving average"
    },
    {
        "KPI_ID": "KPI-002",
        "KPI_Name": "Net Realized Revenue",
        "Domain": "Revenue",
        "Business_Definition": "Actual monetary revenue recognized from settled transactions after subtracting discount deductions and excluding refunds/failed payments.",
        "Formula": "SUM(quantity * unit_price * (1 - discount_pct / 100)) for Paid orders",
        "SQL_Expression": "SUM(CASE WHEN payment_status = 'Paid' THEN quantity * unit_price * (1 - COALESCE(discount_pct, 0)/100.0) ELSE 0 END)",
        "Grain": "Order Line / Daily / Monthly",
        "Filters_Exclusions": "payment_status = 'Paid' only; excludes Pending, Failed, and Refunded transactions.",
        "Business_Owner": "Head of Finance",
        "Technical_Owner": "Analytics Engineer",
        "Refresh_Cadence": "Daily (06:00 UTC)",
        "Target_Benchmark": ">= 85% of Gross Merchandise Value",
        "SLA_Alert_Threshold": "< 75% of GMV or MoM drop > 15%"
    },
    {
        "KPI_ID": "KPI-003",
        "KPI_Name": "Gross Order Volume (Total Placed Orders)",
        "Domain": "Volume",
        "Business_Definition": "Total count of unique checkout attempts placed on the platform regardless of downstream payment settlement status.",
        "Formula": "COUNT(DISTINCT order_id)",
        "SQL_Expression": "COUNT(DISTINCT order_id)",
        "Grain": "Order Header / Daily",
        "Filters_Exclusions": "Exclude technical duplicate rows and corrupted order identifiers.",
        "Business_Owner": "Product Operations Manager",
        "Technical_Owner": "Data Engineering Lead",
        "Refresh_Cadence": "Hourly / Intraday",
        "Target_Benchmark": ">= 50 orders / day",
        "SLA_Alert_Threshold": "Zero orders in 3 consecutive business hours"
    },
    {
        "KPI_ID": "KPI-004",
        "KPI_Name": "Net Completed Orders",
        "Domain": "Volume",
        "Business_Definition": "Total count of successfully settled, active customer purchase orders delivered or provisioned.",
        "Formula": "COUNT(DISTINCT order_id) WHERE payment_status = 'Paid'",
        "SQL_Expression": "COUNT(DISTINCT CASE WHEN payment_status = 'Paid' THEN order_id END)",
        "Grain": "Order Header / Daily",
        "Filters_Exclusions": "Filter strictly for payment_status = 'Paid'.",
        "Business_Owner": "Head of Commercial Operations",
        "Technical_Owner": "Analytics Engineer",
        "Refresh_Cadence": "Daily (06:00 UTC)",
        "Target_Benchmark": ">= 80% of Gross Orders",
        "SLA_Alert_Threshold": "< 70% of Gross Orders"
    },
    {
        "KPI_ID": "KPI-005",
        "KPI_Name": "Payment Success Rate (PSR)",
        "Domain": "Operations",
        "Business_Definition": "Proportion of checkout attempts that complete payment successfully without failure, drop-off, or gateway timeout.",
        "Formula": "(Count of Paid Orders / Total Settled Orders Attempted) * 100",
        "SQL_Expression": "(COUNT(CASE WHEN payment_status = 'Paid' THEN 1 END) * 100.0) / NULLIF(COUNT(order_id), 0)",
        "Grain": "Gateway / Daily Aggregate",
        "Filters_Exclusions": "Exclude automated load tests and verified double-click submissions.",
        "Business_Owner": "Fintech & Payments Lead",
        "Technical_Owner": "Backend Platform Engineer",
        "Refresh_Cadence": "Near Real-Time (15 min)",
        "Target_Benchmark": ">= 85.0%",
        "SLA_Alert_Threshold": "< 75.0% (Trigger P1 Incident)"
    },
    {
        "KPI_ID": "KPI-006",
        "KPI_Name": "Average Order Value (AOV)",
        "Domain": "Commercial",
        "Business_Definition": "The average net monetary spend generated per completed order transaction.",
        "Formula": "Net Realized Revenue / Net Completed Orders",
        "SQL_Expression": "SUM(CASE WHEN payment_status = 'Paid' THEN quantity * unit_price * (1 - COALESCE(discount_pct, 0)/100.0) END) / NULLIF(COUNT(DISTINCT CASE WHEN payment_status = 'Paid' THEN order_id END), 0)",
        "Grain": "Daily / Customer Segment",
        "Filters_Exclusions": "Limited strictly to valid, non-refunded Paid orders.",
        "Business_Owner": "VP of Growth & Commercial Ops",
        "Technical_Owner": "Analytics Engineer",
        "Refresh_Cadence": "Daily (06:00 UTC)",
        "Target_Benchmark": ">= ₹1,200",
        "SLA_Alert_Threshold": "< ₹900"
    },
    {
        "KPI_ID": "KPI-007",
        "KPI_Name": "Discount Depth Rate",
        "Domain": "Commercial",
        "Business_Definition": "Average percentage discount concession provided relative to pre-discount gross catalog revenue across transactions.",
        "Formula": "(Total Discount Concession Amount / Gross Value of Discounted Orders) * 100",
        "SQL_Expression": "SUM(quantity * unit_price * (COALESCE(discount_pct, 0)/100.0)) * 100.0 / NULLIF(SUM(quantity * unit_price), 0)",
        "Grain": "Product Category / Segment Grain",
        "Filters_Exclusions": "Valid orders where discount_pct is between 0% and 100%.",
        "Business_Owner": "Marketing & Growth Director",
        "Technical_Owner": "Analytics Engineer",
        "Refresh_Cadence": "Weekly",
        "Target_Benchmark": "<= 12.0%",
        "SLA_Alert_Threshold": "> 18.0% or unapproved promotional surge"
    },
    {
        "KPI_ID": "KPI-008",
        "KPI_Name": "Refund Rate",
        "Domain": "Customer Experience",
        "Business_Definition": "Proportion of settled transactions reversed due to customer return, cancellation, or fulfillment failure.",
        "Formula": "(Count of Refunded Orders / (Count of Paid + Refunded Orders)) * 100",
        "SQL_Expression": "(COUNT(CASE WHEN payment_status = 'Refunded' THEN 1 END) * 100.0) / NULLIF(COUNT(CASE WHEN payment_status IN ('Paid', 'Refunded') THEN 1 END), 0)",
        "Grain": "Product Category / Monthly Aggregate",
        "Filters_Exclusions": "Requires terminal status tracking (excludes in-flight pending orders).",
        "Business_Owner": "Customer Experience Lead",
        "Technical_Owner": "Data Engineering Lead",
        "Refresh_Cadence": "Daily (06:00 UTC)",
        "Target_Benchmark": "<= 5.0%",
        "SLA_Alert_Threshold": "> 8.0% (Triggers product quality audit)"
    },
    {
        "KPI_ID": "KPI-009",
        "KPI_Name": "Category Revenue Contribution",
        "Domain": "Product Analytics",
        "Business_Definition": "Percentage share of total platform net revenue delivered by each product line (Learning Kit, Course Access, Mentor Session).",
        "Formula": "(Net Revenue per Category / Total Platform Net Revenue) * 100",
        "SQL_Expression": "SUM(CASE WHEN payment_status = 'Paid' THEN quantity * unit_price * (1 - COALESCE(discount_pct, 0)/100.0) END) [per category] / SUM(Total Paid Net Revenue) * 100",
        "Grain": "Product Category / Monthly",
        "Filters_Exclusions": "Paid transactions with standardized product categories.",
        "Business_Owner": "Head of Product Portfolio",
        "Technical_Owner": "BI & Reporting Analyst",
        "Refresh_Cadence": "Weekly",
        "Target_Benchmark": "Balanced Portfolio: Kit ~35%, Course ~45%, Mentor ~20%",
        "SLA_Alert_Threshold": "Any core category declining > 25% MoM"
    },
    {
        "KPI_ID": "KPI-010",
        "KPI_Name": "Customer Segment Penetration & Monetization",
        "Domain": "Customer Strategy",
        "Business_Definition": "Breakdown of completed orders and net revenue contribution across Student, Fresher, and Professional buyer cohorts.",
        "Formula": "Net Revenue & Orders grouped by Customer Segment",
        "SQL_Expression": "GROUP BY customer_segment on Paid orders",
        "Grain": "Customer Segment / Monthly",
        "Filters_Exclusions": "Standardized customer_segment values in ('Student', 'Fresher', 'Professional').",
        "Business_Owner": "VP of Growth & Acquisition",
        "Technical_Owner": "BI & Reporting Analyst",
        "Refresh_Cadence": "Weekly",
        "Target_Benchmark": "Professional segment >= 45% revenue contribution",
        "SLA_Alert_Threshold": "Student cohort share < 20%"
    }
]

df_kpis = pd.DataFrame(kpis)
df_kpis.to_csv(csv_path, index=False)
print(f"Saved CSV to {csv_path}")

# 2. Define Column Data Dictionary Data
columns_meta = [
    {
        "Column_Name": "order_id",
        "Data_Type": "String (Alphanumeric)",
        "Business_Definition": "Unique identifier assigned to each customer order transaction.",
        "Quality_Rule": "Required, Non-null, Unique string matching regex ^RT-[0-9]{4,}$",
        "Acceptable_Values / Range": "Format 'RT-XXXX' (e.g. RT-1001)",
        "Null_Allowed": "No (0% tolerance)",
        "Sample_Anomaly_Found": "Duplicate record for 'RT-1004'"
    },
    {
        "Column_Name": "order_date",
        "Data_Type": "Date (ISO 8601: YYYY-MM-DD)",
        "Business_Definition": "Calendar date on which the customer initiated the order.",
        "Quality_Rule": "Required, valid ISO date between 2025-01-01 and current date.",
        "Acceptable_Values / Range": "2025-01-01 <= Date <= Current Date",
        "Null_Allowed": "No (0% tolerance)",
        "Sample_Anomaly_Found": "Missing date (RT-1011), slash format '03/01/2026' (RT-1002), invalid month '2026-13-10' (RT-1006)"
    },
    {
        "Column_Name": "customer_segment",
        "Data_Type": "Category / String",
        "Business_Definition": "Target demographic group of the customer purchasing ed-tech services.",
        "Quality_Rule": "Must be standardized into Title Case enum: 'Student', 'Fresher', 'Professional'.",
        "Acceptable_Values / Range": "['Student', 'Fresher', 'Professional']",
        "Null_Allowed": "No (< 1% threshold)",
        "Sample_Anomaly_Found": "Lower-case variant 'student' (RT-1003)"
    },
    {
        "Column_Name": "city",
        "Data_Type": "String",
        "Business_Definition": "Billing and shipping metropolitan city of the purchaser.",
        "Quality_Rule": "Required non-empty string, standard city name string length >= 2.",
        "Acceptable_Values / Range": "Valid Indian Metro / Tier-1/2 Cities (e.g. Chennai, Bengaluru)",
        "Null_Allowed": "No (< 2% threshold)",
        "Sample_Anomaly_Found": "Blank / Null city in record RT-1005"
    },
    {
        "Column_Name": "category",
        "Data_Type": "Category / String",
        "Business_Definition": "Product taxonomy family encompassing hardware kits, digital courses, and mentorship.",
        "Quality_Rule": "Must strictly match allowed catalog categories.",
        "Acceptable_Values / Range": "['Learning Kit', 'Course Access', 'Mentor Session']",
        "Null_Allowed": "No (0% tolerance)",
        "Sample_Anomaly_Found": "None (All valid catalog categories)"
    },
    {
        "Column_Name": "quantity",
        "Data_Type": "Integer",
        "Business_Definition": "Number of units of the product category ordered in the line item.",
        "Quality_Rule": "Strict positive integer (> 0), no string word representations.",
        "Acceptable_Values / Range": "Integer >= 1 and <= 50",
        "Null_Allowed": "No (0% tolerance)",
        "Sample_Anomaly_Found": "Negative unit '-1' (RT-1006), spelled-out string 'two' (RT-1008)"
    },
    {
        "Column_Name": "unit_price",
        "Data_Type": "Decimal / Currency (INR)",
        "Business_Definition": "Catalog list price in Indian Rupees (INR) per single unit prior to discount.",
        "Quality_Rule": "Non-negative numeric amount matching standard price points (799, 999, 1499).",
        "Acceptable_Values / Range": "₹799.00 (Kit), ₹999.00 (Mentor), ₹1499.00 (Course)",
        "Null_Allowed": "No (0% tolerance)",
        "Sample_Anomaly_Found": "None (Valid price points observed)"
    },
    {
        "Column_Name": "discount_pct",
        "Data_Type": "Decimal / Percentage",
        "Business_Definition": "Percentage discount concession granted on the catalog price.",
        "Quality_Rule": "Numeric value between 0.0 and 100.0; blank/missing is treated as 0% only after logging.",
        "Acceptable_Values / Range": "0.0 <= discount_pct <= 100.0",
        "Null_Allowed": "Conditional (Missing imputed to 0.0 with warning)",
        "Sample_Anomaly_Found": "Missing discount (RT-1003), Out-of-bounds discount '105%' (RT-1007)"
    },
    {
        "Column_Name": "payment_status",
        "Data_Type": "Category / String",
        "Business_Definition": "Final transaction settlement status returned by payment orchestrator.",
        "Quality_Rule": "Standardized status enum: 'Paid', 'Pending', 'Failed', 'Refunded'.",
        "Acceptable_Values / Range": "['Paid', 'Pending', 'Failed', 'Refunded']",
        "Null_Allowed": "No (0% tolerance)",
        "Sample_Anomaly_Found": "Lower-case 'paid' (RT-1002)"
    }
]

df_cols = pd.DataFrame(columns_meta)

# 3. Define Data Quality Contract Dimension Matrix
dq_rules = [
    {
        "DQ_Dimension": "Completeness",
        "Scope / Target Column": "order_id, order_date, city, payment_status, discount_pct",
        "Quality_Standard": "All mandatory transactional fields must be 100% populated. Missing discount_pct is flagged and defaults to 0.",
        "Failure_Threshold": "> 0% missing in primary keys/dates; > 2% missing in secondary fields.",
        "Action_On_Breach": "P0: Fail pipeline if order_id/order_date missing. P1: Quarantine record and alert ingestion team."
    },
    {
        "DQ_Dimension": "Uniqueness",
        "Scope / Target Column": "order_id",
        "Quality_Standard": "Each order_id must occur exactly once across the active transactional table.",
        "Failure_Threshold": "> 0 duplicate keys detected (Strict 0% tolerance).",
        "Action_On_Breach": "P0: Quarantine duplicates, retain latest valid timestamp or ingest first occurrence and flag duplicate."
    },
    {
        "DQ_Dimension": "Validity (Schema & Range)",
        "Scope / Target Column": "quantity, unit_price, discount_pct, order_date",
        "Quality_Standard": "quantity in Z+ (>0); 0 <= discount_pct <= 100; unit_price > 0; order_date is valid calendar date.",
        "Failure_Threshold": "> 0% invalid types/ranges.",
        "Action_On_Breach": "P1: Quarantine record to anomaly table, log validation error code, alert upstream app engineering."
    },
    {
        "DQ_Dimension": "Consistency",
        "Scope / Target Column": "customer_segment, payment_status, category",
        "Quality_Standard": "Enums must follow strict Title Case standardization ('Paid', 'Pending', 'Failed', 'Refunded'; 'Student', etc.).",
        "Failure_Threshold": "> 1% non-standard casing or invalid category text.",
        "Action_On_Breach": "P2: Apply automated lowercase/strip/title casing transformation during silver stage."
    },
    {
        "DQ_Dimension": "Freshness & Timeliness",
        "Scope / Target Column": "order_date, ingestion_timestamp",
        "Quality_Standard": "Orders must be ingested within 2 hours of placement. Daily batch must complete by 06:00 UTC.",
        "Failure_Threshold": "Ingestion lag > 4 hours or batch completion delay > 30 minutes.",
        "Action_On_Breach": "P1: Trigger PagerDuty notification to Data Platform on-call engineer."
    }
]

df_dq = pd.DataFrame(dq_rules)

# 4. Define Incident Escalation Matrix
escalation_matrix = [
    {
        "Severity_Level": "P0 - Blocker (Critical)",
        "Criteria": "Primary key duplication, missing date on batch > 5%, pipeline crash, corruption in revenue-impacting columns.",
        "Response_SLA": "< 30 Minutes",
        "Resolution_SLA": "< 2 Hours",
        "Escalation_Channel": "PagerDuty + #data-ops-critical Slack channel + SMS to Data Lead",
        "Action_Plan": "Halt downstream marts, prevent corrupt dashboard refreshes, rollback to last verified snapshot, deploy hotfix."
    },
    {
        "Severity_Level": "P1 - High (Major Quality Breach)",
        "Criteria": "Out-of-range quantities/discounts (>100%), payment success rate dropping < 75%, non-critical nulls > 5%.",
        "Response_SLA": "< 1 Hour",
        "Resolution_SLA": "< 6 Hours",
        "Escalation_Channel": "#data-quality-alerts Slack channel + Jira Incident Ticket",
        "Action_Plan": "Quarantine anomalous records into quarantine_orders table, execute data cleansing scripts, notify product team."
    },
    {
        "Severity_Level": "P2 - Medium (Warning / Minor)",
        "Criteria": "Casing inconsistencies (e.g. 'paid' vs 'Paid'), unknown city names, non-blocking schema evolution.",
        "Response_SLA": "< 4 Hours",
        "Resolution_SLA": "< 24 Hours",
        "Escalation_Channel": "#data-eng-backlog Slack + Weekly Quality Review",
        "Action_Plan": "Apply automated normalization transforms, update reference seed tables, refine upstream validation regex."
    }
]

df_escalation = pd.DataFrame(escalation_matrix)

# Create styled Excel Workbook using XlsxWriter
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    workbook = writer.book
    
    # Define Formats
    title_fmt = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'font_color': '#1B365D',
        'align': 'left',
        'valign': 'vcenter'
    })
    
    header_fmt = workbook.add_format({
        'bold': True,
        'font_size': 10,
        'font_color': '#FFFFFF',
        'bg_color': '#1B365D',
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True,
        'border': 1,
        'border_color': '#D3D3D3'
    })
    
    regular_fmt = workbook.add_format({
        'font_size': 9,
        'valign': 'vcenter',
        'text_wrap': True,
        'border': 1,
        'border_color': '#E0E0E0'
    })
    
    zebra_fmt = workbook.add_format({
        'font_size': 9,
        'valign': 'vcenter',
        'text_wrap': True,
        'bg_color': '#F7F9FC',
        'border': 1,
        'border_color': '#E0E0E0'
    })
    
    code_fmt = workbook.add_format({
        'font_name': 'Consolas',
        'font_size': 8.5,
        'font_color': '#0B3C5D',
        'valign': 'vcenter',
        'text_wrap': True,
        'border': 1,
        'border_color': '#E0E0E0'
    })
    
    code_zebra_fmt = workbook.add_format({
        'font_name': 'Consolas',
        'font_size': 8.5,
        'font_color': '#0B3C5D',
        'valign': 'vcenter',
        'text_wrap': True,
        'bg_color': '#F7F9FC',
        'border': 1,
        'border_color': '#E0E0E0'
    })

    def write_custom_sheet(df, sheet_name, title, code_cols=None):
        df.to_excel(writer, sheet_name=sheet_name, startrow=2, index=False)
        worksheet = writer.sheets[sheet_name]
        
        # Write Title
        worksheet.write(0, 0, title, title_fmt)
        worksheet.set_row(0, 28)
        worksheet.set_row(2, 24)
        
        # Format Headers
        for col_num, col_name in enumerate(df.columns):
            worksheet.write(2, col_num, col_name.replace('_', ' '), header_fmt)
            
        # Format Cells
        for r_idx in range(len(df)):
            row_num = r_idx + 3
            worksheet.set_row(row_num, 22)
            is_zebra = (r_idx % 2 == 1)
            for c_idx, col_name in enumerate(df.columns):
                val = df.iloc[r_idx, c_idx]
                is_code = (code_cols and col_name in code_cols)
                
                if is_code:
                    fmt = code_zebra_fmt if is_zebra else code_fmt
                else:
                    fmt = zebra_fmt if is_zebra else regular_fmt
                    
                worksheet.write(row_num, c_idx, str(val) if pd.notna(val) else "", fmt)
                
        # Set Column Widths
        for c_idx, col_name in enumerate(df.columns):
            max_len = max([len(str(val or '')) for val in df[col_name]] + [len(col_name)])
            worksheet.set_column(c_idx, c_idx, min(max(max_len + 4, 15), 45))

    write_custom_sheet(df_kpis, "KPI Dictionary", "RabTech Ed-Commerce - Enterprise KPI Dictionary", ["Formula", "SQL_Expression"])
    write_custom_sheet(df_cols, "Column Data Dictionary", "RabTech Retail Order Schema & Quality Rules", ["Quality_Rule"])
    write_custom_sheet(df_dq, "Data Quality Contract", "Data Quality 5-Dimension Verification Matrix")
    write_custom_sheet(df_escalation, "SLA & Escalation Matrix", "Incident Severity & Escalation Workflow Matrix")

print(f"Successfully generated styled Excel spreadsheet at {excel_path}")
