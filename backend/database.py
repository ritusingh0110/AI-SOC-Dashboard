import sqlite3

connection = sqlite3.connect(
    "soc_dashboard.db"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    port INTEGER,

    failed_attempts INTEGER,

    bytes_sent INTEGER,

    protocol_encoded INTEGER,

    event_encoded INTEGER,

    prediction_code INTEGER,

    severity TEXT
)
""")

connection.commit()

connection.close()

print("Database Ready")