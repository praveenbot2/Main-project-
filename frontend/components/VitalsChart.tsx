"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

export interface VitalsDataPoint {
  time: string;
  heart_rate: number;
  blood_pressure_systolic: number;
  blood_pressure_diastolic: number;
  temperature: number;
  oxygen_saturation: number;
  respiratory_rate: number;
}

interface VitalsChartProps {
  data: VitalsDataPoint[];
}

const LINES = [
  { key: "heart_rate", color: "#ef4444", label: "Heart Rate" },
  { key: "blood_pressure_systolic", color: "#3b82f6", label: "BP Systolic" },
  { key: "blood_pressure_diastolic", color: "#6366f1", label: "BP Diastolic" },
  { key: "oxygen_saturation", color: "#22c55e", label: "SpO₂" },
  { key: "respiratory_rate", color: "#f59e0b", label: "Resp. Rate" },
];

export default function VitalsChart({ data }: VitalsChartProps) {
  if (!data.length) {
    return (
      <div className="flex h-64 items-center justify-center text-sm text-gray-400">
        No data yet — start monitoring to see charts.
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
        <XAxis dataKey="time" tick={{ fontSize: 11 }} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip />
        <Legend />
        {LINES.map(({ key, color, label }) => (
          <Line
            key={key}
            type="monotone"
            dataKey={key}
            name={label}
            stroke={color}
            strokeWidth={2}
            dot={false}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
