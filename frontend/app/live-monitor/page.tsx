"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { motion } from "framer-motion";
import VitalsChart, { type VitalsDataPoint } from "@/components/VitalsChart";
import RiskBanner from "@/components/RiskBanner";
import { getMonitorData } from "@/lib/api";
import type { Condition, Prediction } from "@/lib/types";
import { Play, Square, Activity, Radio } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const CONDITIONS: { value: Condition; label: string }[] = [
  { value: "healthy", label: "Healthy" },
  { value: "at_risk", label: "At Risk" },
  { value: "critical", label: "Critical" },
];

export default function LiveMonitorPage() {
  const [running, setRunning] = useState(false);
  const [condition, setCondition] = useState<Condition>("healthy");
  const [history, setHistory] = useState<VitalsDataPoint[]>([]);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchOnce = useCallback(async () => {
    try {
      const res = await getMonitorData(condition);
      setPrediction(res.prediction);
      const point: VitalsDataPoint = {
        time: new Date(res.timestamp).toLocaleTimeString(),
        ...res.vitals,
      };
      setHistory((prev) => [...prev.slice(-29), point]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Monitor fetch failed");
    }
  }, [condition]);

  function startMonitoring() {
    setRunning(true);
    setError(null);
    fetchOnce();
    intervalRef.current = setInterval(fetchOnce, 3000);
  }

  function stopMonitoring() {
    setRunning(false);
    if (intervalRef.current) clearInterval(intervalRef.current);
  }

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  const latest = history[history.length - 1];

  return (
    <>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
      >
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-500/10 border border-sky-500/20">
            <Activity className="h-5 w-5 text-sky-400" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Live Monitor
            </h1>
            <p className="text-sm text-white/50">
              Real-time simulated vital signs monitoring
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={condition}
            onChange={(e) => setCondition(e.target.value as Condition)}
            className="rounded-lg border border-white/[0.1] bg-white/[0.05] px-3 py-2 text-sm text-white focus:border-teal-500/50 focus:outline-none focus:ring-1 focus:ring-teal-500/30"
          >
            {CONDITIONS.map((c) => (
              <option
                key={c.value}
                value={c.value}
                className="bg-[#04302a] text-white"
              >
                {c.label}
              </option>
            ))}
          </select>

          {running ? (
            <motion.button
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.96 }}
              onClick={stopMonitoring}
              className="flex items-center gap-1.5 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-2 text-sm font-medium text-red-400 transition-colors hover:bg-red-500/20"
            >
              <Square className="h-4 w-4" /> Stop
            </motion.button>
          ) : (
            <motion.button
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.96 }}
              onClick={startMonitoring}
              className="flex items-center gap-1.5 rounded-lg px-4 py-2 text-sm font-medium text-white transition-all"
              style={{
                background: "linear-gradient(135deg, #14B8A6 0%, #0D9488 100%)",
                boxShadow: "0 4px 16px rgba(20,184,166,0.25)",
              }}
            >
              <Play className="h-4 w-4" /> Start
            </motion.button>
          )}

          {running && (
            <div className="flex items-center gap-2">
              <Radio className="h-4 w-4 text-teal-400 animate-pulse" />
              <span className="text-xs text-teal-400/70">Live</span>
            </div>
          )}
        </div>
      </motion.div>

      {error && <p className="mb-4 text-sm text-red-400">{error}</p>}

      {prediction && (
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          className="mb-6"
        >
          <RiskBanner
            riskLevel={prediction.risk_level}
            probability={prediction.probability}
          />
        </motion.div>
      )}

      {/* KPI row */}
      {latest && (
        <div className="mb-6 grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {(
            [
              { label: "HR", value: latest.heart_rate.toFixed(0), unit: "bpm" },
              {
                label: "BP Sys",
                value: latest.blood_pressure_systolic.toFixed(0),
                unit: "mmHg",
              },
              {
                label: "BP Dia",
                value: latest.blood_pressure_diastolic.toFixed(0),
                unit: "mmHg",
              },
              {
                label: "Temp",
                value: latest.temperature.toFixed(1),
                unit: "°C",
              },
              {
                label: "SpO₂",
                value: latest.oxygen_saturation.toFixed(1),
                unit: "%",
              },
              {
                label: "Resp",
                value: latest.respiratory_rate.toFixed(0),
                unit: "br/min",
              },
            ] as const
          ).map((item, i) => (
            <motion.div
              key={item.label}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-4 text-center backdrop-blur-sm"
            >
              <p className="text-[10px] font-semibold uppercase tracking-wider text-teal-400/60">
                {item.label}
              </p>
              <p className="mt-1 text-2xl font-bold text-white">{item.value}</p>
              <Badge variant="secondary" className="mt-1 text-[10px]">
                {item.unit}
              </Badge>
            </motion.div>
          ))}
        </div>
      )}

      {/* Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-6 backdrop-blur-sm"
      >
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-teal-400/60">
          Vitals Timeline
        </h3>
        <VitalsChart data={history} />
      </motion.div>
    </>
  );
}
