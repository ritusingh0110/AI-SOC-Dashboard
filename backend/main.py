from fastapi import FastAPI
from pydantic import BaseModel
from model_loader import rf_model
from save_incident import save_incident
from fastapi.middleware.cors import CORSMiddleware
from threat_intel import get_threat_intel
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from alert_generator import generate_alert
from fastapi import Query
import csv
import sqlite3
app = FastAPI(
    title="AI SOC Dashboard",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

class ThreatInput(BaseModel):

    port: int

    failed_attempts: int

    bytes_sent: int

    protocol_encoded: int

    event_encoded: int
def get_mitre_mapping(port):

    mappings = {
        22: "T1110 - Brute Force",
        3389: "T1021 - Remote Services",
        445: "T1021 - SMB Lateral Movement",
        80: "T1190 - Exploit Public Facing Application"
    }

    return mappings.get(
        port,
        "Unknown Technique"
    )

@app.get("/")
def home():

    return {
        "status": "running"
    }


@app.post("/predict")
def predict_threat(
    data: ThreatInput
):

    features = [[
        data.port,
        data.failed_attempts,
        data.bytes_sent,
        data.protocol_encoded,
        data.event_encoded
    ]]

    prediction = rf_model.predict(
        features
    )
    prediction_code = int(prediction[0])
    severity_map = {
    0: "Critical",
    1: "High",
    2: "Low",
    3: "Medium"
}
    severity = severity_map[prediction_code]
    save_incident(
        data.port,
        data.failed_attempts,
        data.bytes_sent,
        data.protocol_encoded,
        data.event_encoded,
        prediction_code,
        severity
    )
    return {
        "prediction_code": prediction_code,
        "severity": severity,
        "message": "Incident Stored Successfully"
    }
@app.get("/incidents")
def get_incidents():

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM incidents"
    )

    rows = cursor.fetchall()

    connection.close()

    incidents = []

    for row in rows:

        incidents.append({
            "id": row[0],
            "port": row[1],
            "failed_attempts": row[2],
            "bytes_sent": row[3],
            "protocol_encoded": row[4],
            "event_encoded": row[5],
            "prediction_code": row[6],
            "severity": row[7]
        })

    return incidents
@app.get("/total-alerts")
def total_alerts():

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM incidents"
    )

    total = cursor.fetchone()[0]

    connection.close()

    return {
        "total_alerts": total
    }
@app.get("/critical-alerts")
def critical_alerts():

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM incidents
    WHERE severity='Critical'
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return {
        "critical_alerts": count
    }
@app.get("/severity-distribution")
def severity_distribution():

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
    SELECT severity,
           COUNT(*)
    FROM incidents
    GROUP BY severity
    """)

    rows = cursor.fetchall()

    connection.close()

    result = {}

    for row in rows:

        result[row[0]] = row[1]

    return result
@app.get("/risk-score")
def risk_score():

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
    SELECT severity,
           COUNT(*)
    FROM incidents
    GROUP BY severity
    """)

    rows = cursor.fetchall()

    connection.close()

    score = 0

    for severity, count in rows:

        if severity == "Critical":
            score += count * 10

        elif severity == "High":
            score += count * 7

        elif severity == "Medium":
            score += count * 4

        elif severity == "Low":
            score += count * 2

    return {
        "risk_score": score
    }
@app.get("/search")
def search_incidents(
    severity: str = "",
    port: int = 0
):

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    query = """
    SELECT *
    FROM incidents
    WHERE 1=1
    """

    params = []

    if severity:

        query += """
        AND severity = ?
        """

        params.append(
            severity
        )

    if port:

        query += """
        AND port = ?
        """

        params.append(
            port
        )

    cursor.execute(
        query,
        params
    )

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        results.append({
            "id": row[0],
            "port": row[1],
            "failed_attempts": row[2],
            "bytes_sent": row[3],
            "protocol_encoded": row[4],
            "event_encoded": row[5],
            "prediction_code": row[6],
            "severity": row[7],
            "mitre": get_mitre_mapping(row[1])
        })

    return results
@app.get("/search-port")
def search_by_port(port: int):

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM incidents
        WHERE port = ?
    """, (port,))

    rows = cursor.fetchall()

    connection.close()

    incidents = []

    for row in rows:

        incidents.append({
            "id": row[0],
            "port": row[1],
            "failed_attempts": row[2],
            "bytes_sent": row[3],
            "protocol_encoded": row[4],
            "event_encoded": row[5],
            "prediction_code": row[6],
            "severity": row[7],
            "mitre": get_mitre_mapping(row[1])
        })

    return incidents
@app.get("/incident")
def get_incident(incident_id: int):
    

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM incidents
        WHERE id = ?
    """, (incident_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return {
            "message": "Incident not found"
        }

    return {
        "id": row[0],
        "port": row[1],
        "failed_attempts": row[2],
        "bytes_sent": row[3],
        "protocol_encoded": row[4],
        "event_encoded": row[5],
        "prediction_code": row[6],
        "severity": row[7],
        "mitre": get_mitre_mapping(row[1]),
        "threat_intel": get_threat_intel(row[1])
    }
@app.get("/search-id")
def search_id(id: int):

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM incidents
    WHERE id=?
    """, (id,))

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        results.append({
            "id": row[0],
            "port": row[1],
            "failed_attempts": row[2],
            "bytes_sent": row[3],
            "protocol_encoded": row[4],
            "event_encoded": row[5],
            "prediction_code": row[6],
            "severity": row[7],
            "mitre": get_mitre_mapping(row[1])
        })

    return results
def get_mitre_mapping(port):

    if port == 22:
        return "T1110 - Brute Force"

    elif port == 3389:
        return "T1021 - Remote Services"

    elif port == 445:
        return "T1210 - Exploitation"

    else:
        return "Unknown Technique"
@app.get("/top-ports")
def top_ports():

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT port,
               COUNT(*)
        FROM incidents
        GROUP BY port
        ORDER BY COUNT(*) DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()

    connection.close()

    result = []

    for row in rows:

        result.append({
            "port": row[0],
            "count": row[1]
        })

    return result
@app.get("/export-incidents")
def export_incidents():

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM incidents"
    )

    rows = cursor.fetchall()

    connection.close()

    with open(
        "incidents_export.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Port",
            "Failed Attempts",
            "Bytes Sent",
            "Protocol",
            "Event",
            "Prediction",
            "Severity"
        ])

        writer.writerows(rows)

    return FileResponse(
        path="incidents_export.csv",
        filename="incidents_export.csv",
        media_type="text/csv"
    )
@app.get("/generate-report")
def generate_report():

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM incidents
        ORDER BY id DESC
        LIMIT 1
        """
    )

    incident = cursor.fetchone()

    connection.close()

    pdf = SimpleDocTemplate(
        "incident_report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI SOC Incident Report",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            f"Incident ID: {incident[0]}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Port: {incident[1]}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Severity: {incident[7]}",
            styles["BodyText"]
        )
    )

    pdf.build(content)

    return FileResponse(
        "incident_report.pdf",
        filename="incident_report.pdf"
    )
@app.get("/alert")
def get_alert(incident_id: int):

    connection = sqlite3.connect(
        "soc_dashboard.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM incidents WHERE id=?",
        (incident_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if not row:
        return {
            "error": "Incident not found"
        }

    incident = {
        "id": row[0],
        "port": row[1],
        "severity": row[7]
    }

    return {
        "alert": generate_alert(
            incident
        )
    }
@app.get("/send-alert")
def send_alert(email: str):

    return {
        "message": f"Alert sent to {email}"
    }
@app.get("/threat-trends")
def threat_trends():

    conn = sqlite3.connect("soc_dashboard.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT severity, COUNT(*)
        FROM incidents
        GROUP BY severity
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "severity": row[0],
            "count": row[1]
        }
        for row in rows
    ]