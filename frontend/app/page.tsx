"use client";
import SeverityChart from "../components/SeverityChart";

import { useEffect, useState } from "react";

export default function Home() {
 const [threatTrends, setThreatTrends] =
  useState<any[]>([]);
 
 const [liveAlerts, setLiveAlerts] =
  useState<any[]>([]);

const [topPorts, setTopPorts] =
  useState<any[]>([]);

const [selectedIncident, setSelectedIncident] =
  useState<any>(null);

const [incidentId, setIncidentId] =
  useState("");

const [searchPort, setSearchPort] =
  useState("");

const [searchId, setSearchId] =
  useState("");

const [searchSeverity, setSearchSeverity] =
  useState("");

const [email, setEmail] =
  useState("");

const [totalAlerts, setTotalAlerts] =
  useState(0);

const [criticalAlerts, setCriticalAlerts] =
  useState(0);

const [incidents, setIncidents] =
  useState<any[]>([]);

const [riskScore, setRiskScore] =
  useState(0);
  useEffect(() => {

  const loadData = () => {
    fetch("http://127.0.0.1:8000/threat-trends")
  .then((res) => res.json())
  .then((data) => {
    setThreatTrends(data);
  });
    fetch("http://127.0.0.1:8000/top-ports")
  .then((res) => res.json())
  .then((data) => {
    setTopPorts(data);
  });
 

    fetch("http://127.0.0.1:8000/total-alerts")
      .then((res) => res.json())
      .then((data) => {
        setTotalAlerts(data.total_alerts);
      });

    fetch("http://127.0.0.1:8000/critical-alerts")
      .then((res) => res.json())
      .then((data) => {
        setCriticalAlerts(data.critical_alerts);
      });

    fetch("http://127.0.0.1:8000/incidents")
  .then((res) => res.json())
  .then((data) => {

    setIncidents(data);

    setLiveAlerts(
      data.slice(-5).reverse()
    );

  });
    
    fetch("http://127.0.0.1:8000/risk-score")
  .then((res) => res.json())
  .then((data) => {
    setRiskScore(data.risk_score);
  });

  };

  loadData();

  const interval = setInterval(
    loadData,
    5000
  );

  return () => clearInterval(interval);

}, []);

  return (
    <div className="p-10">
      

      <h1 className="text-4xl font-bold mb-8">
        AI SOC Dashboard
      </h1>
      <div className="mb-6">

  <button
    onClick={() => {

      window.open(
        "http://127.0.0.1:8000/export-incidents",
        "_blank"
      );

    }}
    className="bg-indigo-600 text-white px-4 py-2 rounded"
  >
    Export CSV
  </button>
<button
  onClick={() => {

    window.open(
      "http://127.0.0.1:8000/generate-report",
      "_blank"
    );

  }}
  className="ml-3 bg-red-600 text-white px-4 py-2 rounded"
>
  Generate PDF Report
</button>
<div className="mt-4">

  <input
    type="email"
    placeholder="SOC Email"
    value={email}
    onChange={(e) =>
      setEmail(e.target.value)
    }
    className="border p-2 rounded text-black"
  />

 <button
  onClick={() => {

    console.log("EMAIL =", email);

    fetch(
      `http://127.0.0.1:8000/send-alert?email=${email}`
    )
      .then((res) => res.json())
      .then((data) => {

  console.log(data);

  alert(JSON.stringify(data));

});

  }}
  className="ml-3 bg-yellow-600 text-white px-4 py-2 rounded"
>
  Send Alert
</button>

</div>
</div>

      <div className="grid grid-cols-4 gap-6">

        <div className="bg-red-500 text-white p-6 rounded-lg">
          <h2>Total Alerts</h2>

          <p className="text-3xl font-bold">
            {totalAlerts}
          </p>
        </div>

        <div className="bg-orange-500 text-white p-6 rounded-lg">
          <h2>Critical Alerts</h2>

          <p className="text-3xl font-bold">
            {criticalAlerts}
          </p>
        </div>

        <div className="bg-blue-500 text-white p-6 rounded-lg">
          <h2>Risk Score</h2>

          <p className="text-3xl font-bold">
            {riskScore}
          </p>
        </div>
   
        <div className="bg-green-500 text-white p-6 rounded-lg">
          <h2>Incidents</h2>

          <p className="text-3xl font-bold">
            {totalAlerts}
          </p>
        </div>

      </div>
      <div className="mt-10">
    <div className="mt-8">

  <input
    type="text"
    placeholder="Search Severity"
    value={searchSeverity}
    onChange={(e) =>
      setSearchSeverity(e.target.value)
    }
    className="border p-2 rounded"
  />

  <button
    onClick={() => {

      fetch(
        `http://127.0.0.1:8000/search?severity=${searchSeverity}`
      )
        .then((res) => res.json())
        .then((data) => {
          setIncidents(data);
        });

    }}
    className="ml-3 bg-blue-500 text-white px-4 py-2 rounded"
  >
    Search
  </button>

  <button
    onClick={() => {

      fetch(
        "http://127.0.0.1:8000/incidents"
      )
        .then((res) => res.json())
        .then((data) => {
          setIncidents(data);
        });

    }}
    className="ml-3 bg-gray-500 text-white px-4 py-2 rounded"
  >
    Reset
  </button>
<div className="mt-4">

  <input
    type="text"
    placeholder="Search Port"
    value={searchPort}
    onChange={(e) =>
      setSearchPort(e.target.value)
    }
    className="border p-2 rounded"
  />

  <button
    onClick={() => {

      fetch(
        `http://127.0.0.1:8000/search-port?port=${searchPort}`
      )
        .then((res) => res.json())
        .then((data) => {
          setIncidents(data);
        });

    }}
    className="ml-3 bg-green-600 text-white px-4 py-2 rounded"
  >
    Search Port
  </button>

</div>

<div className="mt-4">

  <input
    type="text"
    placeholder="Incident ID"
    value={incidentId}
    onChange={(e) =>
      setIncidentId(e.target.value)
    }
    className="border p-2 rounded"
  />

  <button
    onClick={() => {

      fetch(
        `http://127.0.0.1:8000/incident?incident_id=${incidentId}`
      )
        .then((res) => res.json())
        .then((data) => {

          if(data.id){

            setIncidents([data]);

          }

        });

    }}
    className="ml-3 bg-purple-600 text-white px-4 py-2 rounded"
  >
    
    Search ID
  </button>

</div>

</div>

  <h2 className="text-2xl font-bold mb-4">
    Recent Incidents
  </h2>

  <table className="w-full border">

    <thead>
      <tr className="bg-gray-200">

        <th className="border p-2">ID</th>

        <th className="border p-2">
          Severity
        </th>

        <th className="border p-2">
          Port
        </th>

        <th className="border p-2">
          Failed Attempts
        </th>

      </tr>
    </thead>

    <tbody>

      {Array.isArray(incidents) &&
  incidents.map((incident) => (

        <tr
  key={incident.id}
  className="cursor-pointer hover:bg-gray-100"
  onClick={() => {
    setSelectedIncident(incident);
  }}
>

          <td className="border p-2">
            {incident.id}
          </td>

          <td
  className="border p-2 cursor-pointer text-blue-600"
  onClick={() => {

    alert(`
Incident ID: ${incident.id}

Severity: ${incident.severity}

Port: ${incident.port}

Failed Attempts: ${incident.failed_attempts}
    `);

  }}
>
  {incident.severity}
</td>

          <td className="border p-2">
            {incident.port}
          </td>

          <td className="border p-2">
            {incident.failed_attempts}
          </td>

        </tr>
        

      ))}

    </tbody>

  </table>

</div>
{selectedIncident && (

  <div className="mt-10 p-6 border rounded-lg shadow">

    <h2 className="text-2xl font-bold mb-4">
      Investigation Panel
    </h2>
    

    <p>
      <strong>ID:</strong>
      {" "}
      {selectedIncident.id}
    </p>

    <p>
      <strong>Severity:</strong>
      {" "}
      {selectedIncident.severity}
    </p>

    <p>
      <strong>Port:</strong>
      {" "}
      {selectedIncident.port}
    </p>
    <p>
  <strong>MITRE Technique:</strong>
  {" "}
  {selectedIncident.port === 22
    ? "T1110 - Brute Force"
    : selectedIncident.port === 3389
    ? "T1021 - Remote Services"
    : selectedIncident.port === 445
    ? "T1210 - Exploitation of Remote Services"
    : "Unknown"}
</p>
<p>
  <strong>Threat Intel:</strong>
  {" "}
  {selectedIncident.port === 22
    ? "Known SSH Brute Force Activity"
    : selectedIncident.port === 3389
    ? "RDP Attack Risk"
    : selectedIncident.port === 445
    ? "SMB Exploitation Risk"
    : "No Intelligence Found"}
</p>

    <p>
      <strong>Failed Attempts:</strong>
      {" "}
      {selectedIncident.failed_attempts}
    </p>
<p>
  <strong>MITRE Technique:</strong>
  {selectedIncident.mitre}
</p>
    <p>
      <strong>Bytes Sent:</strong>
      {" "}
      {selectedIncident.bytes_sent}
    </p>

  </div>

)}
<div className="mt-10">

  <h2 className="text-2xl font-bold mb-4">
    Live Alert Feed
  </h2>

  <div className="border rounded p-4">

    {liveAlerts.map((alert) => (

      <div
        key={alert.id}
        className="mb-2 p-2 border-b"
      >

        🚨 {alert.severity}
        {" "}
        Alert on Port
        {" "}
        {alert.port}

      </div>

    ))}

  </div>

</div>
<SeverityChart />
<div className="mt-10">

  <h2 className="text-2xl font-bold mb-4">
    Top Attacked Ports
  </h2>

  <table className="w-full border">

    <thead>
      <tr>
        <th className="border p-2">
          Port
        </th>

        <th className="border p-2">
          Count
        </th>
      </tr>
    </thead>

    <tbody>

      {topPorts.map((port) => (

        <tr key={port.port}>

          <td className="border p-2">
            {port.port}
          </td>

          <td className="border p-2">
            {port.count}
          </td>

        </tr>

      ))}

    </tbody>

  </table>

</div>
<div className="mt-10">

  <h2 className="text-2xl font-bold mb-4">
    Threat Trends Analytics
  </h2>

  <table className="w-full border">

    <thead>

      <tr>

        <th className="border p-2">
          Severity
        </th>

        <th className="border p-2">
          Incident Count
        </th>

      </tr>

    </thead>

    <tbody>

      {threatTrends.map((item) => (

        <tr key={item.severity}>

          <td className="border p-2">
            {item.severity}
          </td>

          <td className="border p-2">
            {item.count}
          </td>

        </tr>

      ))}

    </tbody>

  </table>

</div>

    </div>
  
    
  );
}