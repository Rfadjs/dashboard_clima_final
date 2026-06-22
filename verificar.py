import sqlite3
import pandas as pd

conn = sqlite3.connect("clima.db")

df = pd.read_sql("SELECT * FROM fact_clima", conn)

print(df)

conn.close()