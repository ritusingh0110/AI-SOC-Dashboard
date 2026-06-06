"use client";

import { useEffect, useState } from "react";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function SeverityChart() {
  const [chartData, setChartData] = useState<any>({
  labels: [],
  datasets: [
    {
      label: "Incidents",
      data: [],
    },
  ],
});
  useEffect(() => {
    fetch("http://localhost:8000/severity-distribution")
      .then((response) => response.json())
      .then((data) => {

        setChartData({
          labels: Object.keys(data),

          datasets: [
            {
              label: "Incidents",
              data: Object.values(data),
            },
          ],
        });
      });
  }, []);

  return (
    <div
      style={{
        background: "white",
        padding: "20px",
        borderRadius: "10px",
        marginTop: "30px"
      }}
    >
      <h2>Severity Distribution</h2>

      <Bar data={chartData} />
    </div>
  );
}