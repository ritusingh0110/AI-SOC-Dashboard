import sqlite3
import pandas as pd

connection = sqlite3.connect(
    "soc_dashboard.db"
)

query = """
SELECT *
FROM incidents
"""

df = pd.read_sql_query(
    query,
    connection
)

print(df)

connection.close()
