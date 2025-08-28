# python/load_to_mysql.py
import os
import pandas as pd
from sqlalchemy import create_engine

# ---------- CONFIG ----------
CSV_PATH = "data/SampleSuperstore.csv"
MYSQL_USER = "priyanshi_user"
MYSQL_PASS = "Priyanshi_sql13"   # change this
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "superstore_db"
# ----------------------------

os.makedirs("outputs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

# 1) Load CSV
df = pd.read_csv(CSV_PATH)

# 2) Normalize column names
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('-', '_'))

# 3) Find order_date and ship_date columns (if names vary)
for col in df.columns:
    if 'order' in col and 'date' in col:
        df['order_date'] = pd.to_datetime(df[col], errors='coerce')
        break
for col in df.columns:
    if 'ship' in col and 'date' in col:
        df['ship_date'] = pd.to_datetime(df[col], errors='coerce')
        break

# 4) Connect to MySQL and push table
engine = create_engine("mysql+pymysql://priyanshi_user:Priyanshi_sql13@localhost:3306/superstore_db"
)
df.to_sql(
    'superstore',
    con=engine,
    if_exists='replace',
    index=False,
    chunksize=500,
    method='multi'
)

print("Uploaded to MySQL table 'superstore' in database 'superstore_db'")
