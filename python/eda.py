import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# ---------- CONFIG ----------
MYSQL_USER = "priyanshi_user"       # apna user
MYSQL_PASS = "Priyanshi_sql13"      # apna password
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB   = "superstore_db"
# ----------------------------

# 1) Connect to MySQL
engine = create_engine("mysql+pymysql://priyanshi_user:Priyanshi_sql13@localhost:3306/superstore_db")


# 2) Load data from MySQL table
df = pd.read_sql("SELECT * FROM superstore", con=engine)
print("Data loaded from MySQL:", df.shape)

# 3) Basic info
print(df.head())
print(df.describe())

# 4) Exploratory Data Analysis

# Sales by Category
plt.figure(figsize=(6,4))
sns.barplot(x="category", y="sales", data=df, estimator=sum)
plt.title("Total Sales by Category")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("../screenshots/sales_by_category.png")
plt.close()

# Profit by Region
plt.figure(figsize=(6,4))
sns.barplot(x="region", y="profit", data=df, estimator=sum)
plt.title("Total Profit by Region")
plt.tight_layout()
plt.savefig("../screenshots/profit_by_region.png")
plt.close()

# Monthly Sales Trend
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
monthly_sales = df.groupby(df['order_date'].dt.to_period("M"))['sales'].sum()

plt.figure(figsize=(10,5))
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("../screenshots/monthly_sales_trend.png")
plt.close()

# Sub-Category wise Profit
plt.figure(figsize=(12,5))
sns.barplot(x="sub_category", y="profit", data=df, estimator=sum)
plt.title("Profit by Sub-Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../screenshots/profit_by_subcategory.png")
plt.close()

print("EDA screenshots saved in /screenshots folder ✅")
