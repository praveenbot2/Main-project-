"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import RiskBanner from "@/components/RiskBanner";
import VitalsTable from "@/components/VitalsTable";
import { predictHealth } from "@/lib/api";
import type { Vitals, PredictResponse } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { HeartPulse, Zap } from "lucide-react";

const DEFAULT_VITALS: Vitals = {
  heart_rate: 75,
  blood_pressure_systolic: 120,
  blood_pressure_diastolic: 80,
  temperature: 36.6,
  oxygen_saturation: 98,
  respiratory_rate: 16,
};

const FIELDS: {
  key: keyof Vitals;
  label: string;
  unit: string;
  min: number;
  max: number;
  step: number;
}[] = [
  {
    key: "heart_rate",
    label: "Heart Rate",
    unit: "bpm",
    min: 40,
    max: 200,
    step: 1,
  },
  {
    key: "blood_pressure_systolic",
    label: "BP Systolic",
    unit: "mmHg",
    min: 70,
    max: 200,
    step: 1,
  },
  {
    key: "blood_pressure_diastolic",
    label: "BP Diastolic",
    unit: "mmHg",
    min: 40,
    max: 130,
    step: 1,
  },
  {
    key: "temperature",
    label: "Temperature",
    unit: "°C",
    min: 35,
    max: 42,
    step: 0.1,
  },
  {
    key: "oxygen_saturation",
    label: "SpO₂",
    unit: "%",
    min: 70,
    max: 100,
    step: 0.1,
  },
  {
    key: "respiratory_rate",
    label: "Resp. Rate",
    unit: "br/min",
    min: 8,
    max: 40,
    step: 1,
  },
];

export default function HealthCheckPage() {
  const [vitals, setVitals] = useState<Vitals>({ ...DEFAULT_VITALS });
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await predictHealth(vitals);
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  function handleChange(key: keyof Vitals, val: string) {
    setVitals((prev) => ({ ...prev, [key]: parseFloat(val) || 0 }));
  }

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8 flex items-center gap-3"
      >
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-500/10 border border-teal-500/20">
          <HeartPulse className="h-5 w-5 text-teal-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Health Check
          </h1>
          <p className="text-sm text-white/50">
            Enter vital signs to get an AI-powered health risk prediction
          </p>
        </div>
      </motion.div>

      <div className="grid gap-8 lg:grid-cols-2">
        {/* Form */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <div className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-6 backdrop-blur-sm">
            <h2 className="mb-5 text-sm font-semibold uppercase tracking-wider text-teal-400/60">
              Enter Vital Signs
            </h2>
            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid gap-4 sm:grid-cols-2">
                {FIELDS.map(({ key, label, unit, min, max, step }) => (
                  <div key={key}>
                    <label className="mb-1.5 block text-sm font-medium text-white/60">
                      {label}{" "}
                      <span className="text-xs text-white/30">({unit})</span>
                    </label>
                    <input
                      type="number"
                      min={min}
                      max={max}
                      step={step}
                      value={vitals[key]}
                      onChange={(e) => handleChange(key, e.target.value)}
                      className="w-full rounded-lg border border-white/[0.1] bg-white/[0.05] px-3 py-2.5 text-sm text-white placeholder:text-white/30 focus:border-teal-500/50 focus:outline-none focus:ring-1 focus:ring-teal-500/30 transition-colors"
                    />
                  </div>
                ))}
              </div>

              <motion.button
                type="submit"
                disabled={loading}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex w-full items-center justify-center gap-2 rounded-xl py-3.5 text-sm font-semibold text-white transition-all disabled:opacity-50"
                style={{
                  background:
                    "linear-gradient(135deg, #14B8A6 0%, #0D9488 100%)",
                  boxShadow: "0 4px 24px rgba(20,184,166,0.3)",
                }}
              >
                <Zap className="h-4 w-4" />
                {loading ? "Analyzing…" : "Analyze Vitals"}
              </motion.button>

              {error && <p className="text-sm text-red-400">{error}</p>}
            </form>
          </div>
        </motion.div>

        {/* Result */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="space-y-5"
        >
          {result ? (
            <>
              <RiskBanner
                riskLevel={result.prediction.risk_level}
                probability={result.prediction.probability}
                message={result.alert.message}
              />

              <VitalsTable vitals={result.vitals} />

              {result.prediction.recommendations.length > 0 && (
                <div className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 backdrop-blur-sm">
                  <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-teal-400/60">
                    Recommendations
                  </h3>
                  <ul className="space-y-2">
                    {result.prediction.recommendations.map((r, i) => (
                      <li
                        key={i}
                        className="flex items-start gap-2 text-sm text-white/60"
                      >
                        <Badge
                          variant="success"
                          className="mt-0.5 shrink-0 text-[10px]"
                        >
                          {i + 1}
                        </Badge>
                        {r}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          ) : (
            <div className="flex h-64 flex-col items-center justify-center gap-3 rounded-xl border border-dashed border-white/[0.1] text-sm text-white/30">
              <HeartPulse className="h-8 w-8 text-teal-500/30" />
              Submit vitals to see prediction results
            </div>
          )}
        </motion.div>
      </div>
    </>
  );
}
