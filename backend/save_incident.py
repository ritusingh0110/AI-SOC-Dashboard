import sqlite3

def save_incident(
    port,
    failed_attempts,
    bytes_sent,
    protocol_encoded,
    event_encoded,
    prediction_code,
    severity
):

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO incidents (

        port,
        failed_attempts,
        bytes_sent,
        protocol_encoded,
        event_encoded,
        prediction_code,
        severity

    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        port,
        failed_attempts,
        bytes_sent,
        protocol_encoded,
        event_encoded,
        prediction_code,
        severity
    ))

    connection.commit()

    connection.close()