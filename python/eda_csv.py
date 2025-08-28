# python/eda_csv.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("outputs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

CSV_PATH = "data/SampleSuperstore.csv"  # change if filename different

# 1) load & normalize columns
df = pd.read_csv(CSV_PATH)
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('-', '_'))

# 2) parse dates (detect order date column)
order_col = None
for c in df.columns:
    if 'order' in c and 'date' in c:
        order_col = c
        break
if order_col:
    df['order_date'] = pd.to_datetime(df[order_col], errors='coerce')
else:
    print("Warning: order date column not found. Monthly trend may not work.")

# 3) Aggregations
# Sales by region
if 'region' in df.columns and 'sales' in df.columns:
    region_sales = df.groupby('region', dropna=False)['sales'].sum().reset_index().sort_values('sales', ascending=False)
    region_sales.to_csv("outputs/region_sales.csv", index=False)
else:
    print("region or sales column missing in CSV")

# Top subcategories by profit
if 'sub_category' in df.columns and 'profit' in df.columns:
    top_sub = df.groupby('sub_category')['profit'].sum().reset_index().sort_values('profit', ascending=False).head(10)
    top_sub.to_csv("outputs/top_subcategories_profit.csv", index=False)
else:
    print("sub_category or profit column missing")

# Monthly sales trend
if 'order_date' in df.columns:
    monthly = df.dropna(subset=['order_date']).groupby(df['order_date'].dt.to_period('M'))['sales'].sum().reset_index()
    monthly['month'] = monthly['order_date'].dt.to_timestamp()
    monthly = monthly.rename(columns={'sales':'monthly_sales'})
    monthly[['month','monthly_sales']].to_csv("outputs/monthly_sales.csv", index=False)
else:
    print("Monthly sales not computed due to missing order_date")

# 4) Plots
sns.set(style="whitegrid")
if 'region_sales' in locals():
    plt.figure(figsize=(8,5))
    sns.barplot(x='sales', y='region', data=region_sales)
    plt.title('Sales by Region')
    plt.tight_layout()
    plt.savefig("screenshots/sales_by_region.png")
    plt.close()

if 'top_sub' in locals():
    plt.figure(figsize=(10,6))
    sns.barplot(x='profit', y='sub_category', data=top_sub)
    plt.title('Top 10 Subcategories by Profit')
    plt.tight_layout()
    plt.savefig("screenshots/top_subcategories_profit.png")
    plt.close()

if 'monthly' in locals():
    plt.figure(figsize=(10,4))
    plt.plot(monthly['month'], monthly['monthly_sales'], marker='o')
    plt.title('Monthly Sales Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("screenshots/monthly_trend.png")
    plt.close()

print("Done. Check outputs/ and screenshots/")
