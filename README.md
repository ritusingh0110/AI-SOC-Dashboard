# AI-Powered SOC Dashboard

An end-to-end Security Operations Center (SOC) Dashboard that combines Cybersecurity Analytics, Threat Detection, Machine Learning, Threat Intelligence, MITRE ATT&CK Mapping, Incident Investigation, and Reporting into a single platform.

The project simulates how modern SOC teams monitor, investigate, and respond to security incidents using both traditional security analytics and machine learning.

---

## Project Overview

This dashboard was built to demonstrate practical cybersecurity engineering and machine learning integration in a Security Operations Center environment.

The system ingests security event data, classifies threats using machine learning, stores incidents, visualizes security metrics, and provides investigation capabilities for analysts.

---

## Features

### Security Monitoring

* Real-time Incident Dashboard
* Total Alert Monitoring
* Critical Alert Monitoring
* Live Alert Feed
* Threat Trend Monitoring
* Risk Score Calculation

### Incident Investigation

* Search by Severity
* Search by Port
* Search by Incident ID
* Incident Investigation Panel
* Threat Context Display

### Threat Intelligence

* MITRE ATT&CK Technique Mapping
* Threat Intelligence Mapping
* Port-Based Threat Analysis
* Attack Surface Visibility

### Analytics

* Severity Distribution Chart
* Top Attacked Ports
* Threat Trend Visualization
* Risk Scoring Engine

### Reporting

* CSV Export
* PDF Incident Report Generation
* SOC Alert Workflow

---

# Machine Learning Integration

The platform incorporates machine learning models for automated threat detection and anomaly analysis.

## Threat Detection Model

Algorithm:

* Random Forest Classifier

Purpose:

* Classifies incoming security events into threat severity levels.
* Supports automated incident prioritization.

Input Features:

* Port Number
* Failed Login Attempts
* Bytes Sent
* Protocol Type (Encoded)
* Event Type (Encoded)

Output Classes:

* Critical
* High
* Medium
* Low

## Anomaly Detection Model

Algorithm:

* Isolation Forest

Purpose:

* Detects unusual network activity patterns.
* Identifies behaviors that deviate from normal traffic baselines.

The anomaly detection model is included as part of the ML architecture and can be used alongside threat classification for advanced threat hunting workflows.

---

# System Architecture

Security Logs

↓

FastAPI Backend

↓

Machine Learning Models

* Random Forest Classifier
* Isolation Forest

↓

SQLite Incident Database

↓

Next.js SOC Dashboard

↓

SOC Analyst Investigation

---

# Tech Stack

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

## Backend

* FastAPI
* Python
* SQLite

## Machine Learning

* Scikit-Learn
* Random Forest Classifier
* Isolation Forest
* Joblib

## Data Processing

* Pandas
* NumPy

## Reporting

* ReportLab
* CSV Export

---

# Project Structure

```text
AI-SOC-Dashboard/

├── backend/
│   ├── main.py
│   ├── database.py
│   ├── model_loader.py
│   ├── risk_engine.py
│   ├── threat_intel.py
│   ├── save_incident.py
│   ├── alert_generator.py
│   ├── threat_detection_model.pkl
│   ├── anomaly_model.pkl
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│
├── data/
│   ├── security_logs.csv
│   ├── soc_logs.csv
│
└── README.md
```

---

# API Endpoints

## Threat Detection

POST /predict

Predict threat severity using machine learning.

---

## Incident Management

GET /incidents

Retrieve stored incidents.

GET /incident

Retrieve incident by ID.

GET /search

Search incidents by severity.

GET /search-port

Search incidents by destination port.

GET /search-id

Search incidents by incident ID.

---

## Analytics

GET /total-alerts

GET /critical-alerts

GET /severity-distribution

GET /risk-score

GET /top-ports

GET /threat-trends

---

## Reporting

GET /export-incidents

Export incidents as CSV.

GET /generate-report

Generate PDF report.

---

# Machine Learning Training

The machine learning models were trained using Scikit-Learn.

Training workflow:

1. Security log dataset generation
2. Feature engineering
3. Label preparation
4. Model training
5. Model serialization using Joblib
6. FastAPI deployment

Models were trained and exported as:

* threat_detection_model.pkl
* anomaly_model.pkl

---

# How To Run

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

# Key Learning Outcomes

* Security Operations Center (SOC) Workflows
* Threat Detection Engineering
* Machine Learning for Cybersecurity
* Threat Intelligence Integration
* MITRE ATT&CK Mapping
* FastAPI Backend Development
* Next.js Dashboard Development
* Security Analytics
* Incident Investigation Workflows
* Security Reporting Automation

---

# Future Improvements

* Real-Time WebSocket Alerts
* Email Notification Integration
* SIEM Integration
* Threat Hunting Module
* User Authentication
* Role-Based Access Control
* Cloud Deployment
* Advanced Anomaly Detection Pipeline

---

# Author

Ritu Singh

Cybersecurity | Machine Learning | Security Analytics
