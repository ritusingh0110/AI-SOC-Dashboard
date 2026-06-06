# AI-Powered SOC Dashboard

An AI-driven Security Operations Center (SOC) Dashboard built using FastAPI, Next.js, Machine Learning, and SQLite.

## Features

* Real-time Incident Monitoring
* Threat Severity Classification
* Risk Score Calculation
* MITRE ATT&CK Technique Mapping
* Threat Intelligence Mapping
* Live Alert Feed
* Search by Severity
* Search by Port
* Search by Incident ID
* Top Attacked Ports Analytics
* CSV Export
* PDF Report Generation
* SOC Alert Notification System
* Threat Trend Analysis

## Tech Stack

### Backend

* FastAPI
* SQLite
* Scikit-Learn
* Pandas

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

## Dashboard Capabilities

* Analyze security incidents
* Investigate threats through MITRE ATT&CK mapping
* Monitor attack trends
* Generate security reports
* Export incident data
* Track risk posture

## Project Structure

backend/
frontend/
data/

## Running the Project

Backend:

```bash
cd backend
uvicorn main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend URL:

http://127.0.0.1:8000

Frontend URL:

http://localhost:3000

## Future Enhancements

* SIEM Integration
* Email Notifications
* Threat Intelligence API Integration
* User Authentication
* Real-Time WebSocket Alerts

## Author

Ritu Singh
