import sqlite3
import random

conn = sqlite3.connect("soc_dashboard.db")
cursor = conn.cursor()

for i in range(200):

    severity = random.choice([
        "Low",
        "Medium",
        "High",
        "Critical"
    ])

    port = random.choice([
        22,
        80,
        443,
        445,
        3389
    ])

    failed_attempts = random.randint(
        1,
        30
    )

    bytes_sent = random.randint(
        100,
        10000
    )

    cursor.execute("""
    INSERT INTO incidents
    (
        severity,
        port,
        failed_attempts,
        bytes_sent
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        severity,
        port,
        failed_attempts,
        bytes_sent
    ))

conn.commit()
conn.close()

print("Done")