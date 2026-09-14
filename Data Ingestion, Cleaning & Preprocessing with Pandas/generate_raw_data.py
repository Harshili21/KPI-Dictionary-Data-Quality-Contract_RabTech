import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

N_ROWS = 12500

# 1. Product Catalog Definition
categories = {
    'Electronics': [
        ('Smartphone Pro', 799.99, 450.0),
        ('Wireless Earbuds', 129.99, 45.0),
        ('4K Ultra Monitor', 349.99, 190.0),
        ('Gaming Mechanical Keyboard', 89.99, 35.0),
        ('USB-C Fast Charger', 29.99, 8.5)
    ],
    'Home & Kitchen': [
        ('Espresso Coffee Maker', 199.99, 90.0),
        ('Stainless Steel Cookware Set', 149.99, 65.0),
        ('Air Purifier HEPA', 119.99, 50.0),
        ('Robot Vacuum Cleaner', 299.99, 130.0),
        ('Blender & Smoothie Maker', 59.99, 22.0)
    ],
    'Clothing & Apparel': [
        ('Waterproof Winter Jacket', 120.00, 48.0),
        ('Slim-Fit Denim Jeans', 65.00, 24.0),
        ('Merino Wool Sweater', 85.00, 32.0),
        ('Breathable Running Shoes', 110.00, 42.0),
        ('Casual Cotton T-Shirt', 25.00, 7.0)
    ],
    'Beauty & Personal Care': [
        ('Vitamin C Facial Serum', 35.00, 10.0),
        ('Ionic Hair Dryer', 75.00, 28.0),
        ('Organic Moisturizing Cream', 28.00, 8.0),
        ('Sonic Electric Toothbrush', 49.99, 16.0),
        ('Sunscreen SPF 50+', 22.00, 6.0)
    ],
    'Books & Stationery': [
        ('Hardcover Productivity Journal', 18.50, 4.5),
        ('Data Science Handbook (Hardcover)', 54.99, 20.0),
        ('Ergonomic Fountain Pen Set', 32.00, 9.0),
        ('Business Strategy Guide', 24.99, 6.0),
        ('Artist Sketchbook Pack', 15.00, 3.5)
    ]
}

category_names = list(categories.keys())

# Customer Segments & Regions
regions = ['United States', 'USA', 'U.S.A.', 'united states', 'Canada', 'CA', 'United Kingdom', 'UK', 'U.K.', 'Germany', 'germany', 'France', 'Australia', 'Japan', 'India', 'IN']
genders = ['Male', 'M', 'm', 'Female', 'FEMALE', 'f', 'Non-Binary', 'Other', None]
payment_methods = ['Credit Card', 'credit card', 'PayPal', 'PAYPAL', 'Debit Card', 'Cash on Delivery', 'Bank Transfer', 'Apple Pay', None]
order_statuses = ['Delivered', 'delivered', 'Shipped', 'shipped', 'Processing', 'Cancelled', 'Refunded', 'Returned']

# Generate base data
data = []
start_date = datetime(2024, 1, 1)

for i in range(1, N_ROWS + 1):
    order_id = f"ORD-{100000 + i}"
    cust_id = f"CUST-{random.randint(1001, 3500)}"
    
    # Category & Product
    cat = random.choice(category_names)
    prod, unit_price_base, cost_base = random.choice(categories[cat])
    
    # Dates
    random_days = random.randint(0, 700) # spanning 2024 to early 2026
    order_dt = start_date + timedelta(days=random_days)
    ship_delay = random.randint(1, 7)
    ship_dt = order_dt + timedelta(days=ship_delay)
    
    # Date formatting mix
    fmt_choice = random.random()
    if fmt_choice < 0.70:
        order_dt_str = order_dt.strftime('%Y-%m-%d')
        ship_dt_str = ship_dt.strftime('%Y-%m-%d')
    elif fmt_choice < 0.85:
        order_dt_str = order_dt.strftime('%d/%m/%Y')
        ship_dt_str = ship_dt.strftime('%d/%m/%Y')
    elif fmt_choice < 0.95:
        order_dt_str = order_dt.strftime('%m-%d-%Y')
        ship_dt_str = ship_dt.strftime('%m-%d-%Y')
    else:
        # Invalid date or missing
        if random.random() < 0.5:
            order_dt_str = "2025-02-31" # invalid day
            ship_dt_str = "2025-03-05"
        else:
            order_dt_str = None
            ship_dt_str = ship_dt.strftime('%Y-%m-%d')
            
    # Ship date before order date anomaly (0.5% chance)
    if random.random() < 0.005 and order_dt_str:
        ship_dt_str = (order_dt - timedelta(days=3)).strftime('%Y-%m-%d')
        
    # Customer Details
    cust_name = f"Customer_{cust_id.split('-')[1]}"
    if random.random() < 0.15:
        cust_name = cust_name.lower() if random.random() < 0.5 else f"  {cust_name.upper()}  "
        
    age = random.randint(18, 75)
    # Age anomalies
    if random.random() < 0.015:
        age = random.choice([-5, -1, 150, 999, 0])
    elif random.random() < 0.03:
        age = None
        
    gender = random.choice(genders)
    region = random.choice(regions)
    if random.random() < 0.02:
        region = None
        
    # Quantity with noise
    qty = random.randint(1, 8)
    if random.random() < 0.01:
        qty_str = random.choice(['two', 'three', 'one', '-1', '-3', '0'])
    elif random.random() < 0.02:
        qty_str = None
    elif random.random() < 0.005:
        qty_str = random.randint(150, 500) # massive quantity outlier
    else:
        qty_str = str(qty) if random.random() < 0.3 else qty
        
    # Unit price with noise (symbols, strings)
    price_val = round(unit_price_base * random.uniform(0.95, 1.05), 2)
    if random.random() < 0.08:
        price_str = f"${price_val:.2f}"
    elif random.random() < 0.02:
        price_str = f"€{price_val:.2f}"
    elif random.random() < 0.005:
        price_str = -price_val # negative price anomaly
    elif random.random() < 0.015:
        price_str = None
    else:
        price_str = price_val
        
    # Discount
    disc = random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
    if random.random() < 0.10:
        disc_str = f"{int(disc*100)}%"
    elif random.random() < 0.005:
        disc_str = 1.5 # 150% discount outlier
    elif random.random() < 0.04:
        disc_str = None
    else:
        disc_str = disc
        
    # Shipping Cost
    ship_cost = round(random.uniform(4.99, 25.00), 2)
    if random.random() < 0.03:
        ship_cost = None
    elif random.random() < 0.005:
        ship_cost = -10.0
        
    pay_method = random.choice(payment_methods)
    status = random.choice(order_statuses)
    cost = round(cost_base, 2)
    
    data.append({
        'Transaction_ID': order_id,
        'Order_Date': order_dt_str,
        'Ship_Date': ship_dt_str,
        'Customer_ID': cust_id,
        'Customer_Name': cust_name,
        'Customer_Age': age,
        'Customer_Gender': gender,
        'Customer_Region': region,
        'Product_Category': cat,
        'Product_Name': prod,
        'Quantity_Ordered': qty_str,
        'Unit_Price': price_str,
        'Unit_Cost': cost,
        'Discount_Applied': disc_str,
        'Shipping_Cost': ship_cost,
        'Payment_Method': pay_method,
        'Order_Status': status
    })

df = pd.DataFrame(data)

# Inject Duplicate Rows (~350 duplicate transactions to simulate pipeline retries)
dup_indices = random.sample(range(len(df)), 350)
dup_df = df.iloc[dup_indices].copy()
# slightly corrupt some duplicates
full_df = pd.concat([df, dup_df], ignore_index=True)

# Shuffle dataset
full_df = full_df.sample(frac=1.0, random_state=42).reset_index(drop=True)

csv_path = r"c:\Users\Harshili\Desktop\RabTech\Data Ingestion, Cleaning & Preprocessing with Pandas\raw_business_dataset.csv"
full_df.to_csv(csv_path, index=False)
print(f"Generated realistic messy dataset with {len(full_df)} rows and {len(full_df.columns)} columns at {csv_path}")
