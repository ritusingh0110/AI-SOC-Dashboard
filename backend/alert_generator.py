# backend/alert_generator.py

def generate_alert(incident):

    return f"""
SOC ALERT

Incident ID: {incident["id"]}
Severity: {incident["severity"]}
Port: {incident["port"]}

Recommended Action:
Review logs immediately.
"""