"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getMonitorData, getHealthCheck } from "@/lib/api";
import type { Vitals, Prediction } from "@/lib/types";
import {
  HeartPulse,
  Thermometer,
  Wind,
  Droplets,
  Activity,
  Server,
  ShieldCheck,
  ArrowRight,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BentoCard, BentoGrid } from "@/components/ui/bento-grid";
import RiskBanner from "@/components/RiskBanner";
import VitalsTable from "@/components/VitalsTable";
import Link from "next/link";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  show: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.5 },
  }),
};

function KpiMetric({
  label,
  value,
  unit,
  icon,
  index,
}: {
  label: string;
  value: string;
  unit: string;
  icon: React.ReactNode;
  index: number;
}) {
  return (
    <motion.div
      custom={index}
      variants={fadeUp}
      initial="hidden"
      animate="show"
    >
      <div className="group relative rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 backdrop-blur-sm transition-all hover:border-teal-500/30 hover:bg-white/[0.05]">
        <div className="flex items-center justify-between">
          <span className="text-[10px] font-semibold uppercase tracking-wider text-teal-400/60">
            {label}
          </span>
          <span className="text-teal-400/40 group-hover:text-teal-400/70 transition-colors">
            {icon}
          </span>
        </div>
        <div className="mt-3 flex items-baseline gap-1">
          <span className="text-3xl font-bold text-white">{value}</span>
          <span className="text-sm text-white/40">{unit}</span>
        </div>
      </div>
    </motion.div>
  );
}

export default function DashboardPage() {
  const [vitals, setVitals] = useState<Vitals | null>(null);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);

  async function fetchData() {
    try {
      const health = await getHealthCheck();
      setBackendOnline(health.status === "healthy");
    } catch {
      setBackendOnline(false);
    }
    try {
      const res = await getMonitorData("healthy");
      setVitals(res.vitals);
      setPrediction(res.prediction);
    } catch {
      /* backend may be down */
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
    const id = setInterval(fetchData, 10000);
    return () => clearInterval(id);
  }, []);

  return (
    <>
      {/* Page header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Dashboard
          </h1>
          <p className="text-sm text-white/50">
            Overview of your health monitoring system
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge
            variant={
              backendOnline === null
                ? "secondary"
                : backendOnline
                  ? "success"
                  : "danger"
            }
            className="gap-1.5"
          >
            <Server className="h-3 w-3" />
            {backendOnline === null
              ? "Checking…"
              : backendOnline
                ? "Backend Online"
                : "Backend Offline"}
          </Badge>
          <Link
            href="/"
            className="text-xs text-teal-400/60 hover:text-teal-400 transition-colors flex items-center gap-1"
          >
            Landing Page <ArrowRight className="h-3 w-3" />
          </Link>
        </div>
      </motion.div>

      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <div className="flex flex-col items-center gap-3">
            <div className="h-8 w-8 animate-spin rounded-full border-2 border-teal-500/30 border-t-teal-400" />
            <span className="text-sm text-white/40">Loading data…</span>
          </div>
        </div>
      ) : (
        <>
          {/* KPI Cards */}
          {vitals && (
            <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
              <KpiMetric
                index={0}
                label="Heart Rate"
                value={vitals.heart_rate.toFixed(0)}
                unit="bpm"
                icon={<HeartPulse className="h-5 w-5" />}
              />
              <KpiMetric
                index={1}
                label="BP Systolic"
                value={vitals.blood_pressure_systolic.toFixed(0)}
                unit="mmHg"
                icon={<Activity className="h-5 w-5" />}
              />
              <KpiMetric
                index={2}
                label="BP Diastolic"
                value={vitals.blood_pressure_diastolic.toFixed(0)}
                unit="mmHg"
                icon={<Activity className="h-5 w-5" />}
              />
              <KpiMetric
                index={3}
                label="Temperature"
                value={vitals.temperature.toFixed(1)}
                unit="°C"
                icon={<Thermometer className="h-5 w-5" />}
              />
              <KpiMetric
                index={4}
                label="SpO₂"
                value={vitals.oxygen_saturation.toFixed(1)}
                unit="%"
                icon={<Droplets className="h-5 w-5" />}
              />
              <KpiMetric
                index={5}
                label="Resp. Rate"
                value={vitals.respiratory_rate.toFixed(0)}
                unit="br/min"
                icon={<Wind className="h-5 w-5" />}
              />
            </div>
          )}

          {/* Risk Banner */}
          {prediction && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.5 }}
              className="mb-8"
            >
              <RiskBanner
                riskLevel={prediction.risk_level}
                probability={prediction.probability}
                message={prediction.recommendations?.[0]}
              />
            </motion.div>
          )}

          {/* Bento feature grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            <BentoGrid className="mb-8 lg:grid-rows-2 lg:grid-cols-3 auto-rows-[14rem]">
              <BentoCard
                name="Health Check"
                className="lg:col-span-1"
                Icon={HeartPulse}
                description="Run an AI-powered analysis on your vitals"
                href="/health-check"
                cta="Check now"
                background={
                  <div className="absolute inset-0 bg-gradient-to-br from-teal-500/10 to-transparent" />
                }
              />
              <BentoCard
                name="Live Monitoring"
                className="lg:col-span-1"
                Icon={Activity}
                description="Real-time simulated vital signs with charts"
                href="/live-monitor"
                cta="Start monitoring"
                background={
                  <div className="absolute inset-0 bg-gradient-to-br from-sky-500/10 to-transparent" />
                }
              />
              <BentoCard
                name="AI Chat"
                className="lg:col-span-1"
                Icon={ShieldCheck}
                description="Talk to the health assistant about symptoms"
                href="/chat"
                cta="Open chat"
                background={
                  <div className="absolute inset-0 bg-gradient-to-br from-violet-500/10 to-transparent" />
                }
              />
            </BentoGrid>
          </motion.div>

          {/* Vitals Table */}
          {vitals && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.5 }}
            >
              <div className="rounded-xl border border-white/[0.08] bg-white/[0.02] p-6 backdrop-blur-sm">
                <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-teal-400/60">
                  Current Vitals
                </h3>
                <VitalsTable vitals={vitals} />
              </div>
            </motion.div>
          )}
        </>
      )}
    </>
  );
}
