"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getAlerts } from "@/lib/api";
import {
  AlertCircle,
  AlertTriangle,
  Info,
  RefreshCw,
  Bell,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import type { Alert } from "@/lib/types";

interface AlertSummary {
  total_alerts: number;
  critical_alerts: number;
  warning_alerts: number;
  info_alerts: number;
  recent_alerts: Alert[];
}

const fadeUp = {
  hidden: { opacity: 0, y: 15 },
  show: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.4 },
  }),
};

export default function AlertsPage() {
  const [summary, setSummary] = useState<AlertSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchAlerts() {
    setLoading(true);
    setError(null);
    try {
      const res = await getAlerts();
      setSummary(res.alerts);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch alerts");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchAlerts();
  }, []);

  const ICON_MAP: Record<string, typeof AlertCircle> = {
    CRITICAL: AlertCircle,
    WARNING: AlertTriangle,
    INFO: Info,
  };

  const SUMMARY_CARDS = summary
    ? [
        {
          label: "Total",
          value: summary.total_alerts,
          color: "text-white/60",
          bg: "bg-white/[0.03]",
          border: "border-white/[0.08]",
        },
        {
          label: "Critical",
          value: summary.critical_alerts,
          color: "text-red-400",
          bg: "bg-red-500/5",
          border: "border-red-500/15",
        },
        {
          label: "Warning",
          value: summary.warning_alerts,
          color: "text-amber-400",
          bg: "bg-amber-500/5",
          border: "border-amber-500/15",
        },
        {
          label: "Info",
          value: summary.info_alerts,
          color: "text-emerald-400",
          bg: "bg-emerald-500/5",
          border: "border-emerald-500/15",
        },
      ]
    : [];

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
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10 border border-amber-500/20">
            <Bell className="h-5 w-5 text-amber-400" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Alerts
            </h1>
            <p className="text-sm text-white/50">
              View alert history and summary
            </p>
          </div>
        </div>
        <motion.button
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.96 }}
          onClick={fetchAlerts}
          disabled={loading}
          className="flex items-center gap-1.5 rounded-lg border border-white/[0.1] bg-white/[0.05] px-4 py-2 text-sm font-medium text-white/70 transition-colors hover:bg-white/[0.08] disabled:opacity-50"
        >
          <RefreshCw className={cn("h-4 w-4", loading && "animate-spin")} />
          Refresh
        </motion.button>
      </motion.div>

      {error && <p className="mb-4 text-sm text-red-400">{error}</p>}

      {loading && !summary ? (
        <div className="flex h-64 items-center justify-center">
          <div className="flex flex-col items-center gap-3">
            <div className="h-8 w-8 animate-spin rounded-full border-2 border-teal-500/30 border-t-teal-400" />
            <span className="text-sm text-white/40">Loading alerts…</span>
          </div>
        </div>
      ) : summary ? (
        <>
          {/* Summary cards */}
          <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {SUMMARY_CARDS.map((item, i) => (
              <motion.div
                key={item.label}
                custom={i}
                variants={fadeUp}
                initial="hidden"
                animate="show"
              >
                <div
                  className={cn(
                    "rounded-xl border p-5 backdrop-blur-sm",
                    item.bg,
                    item.border,
                  )}
                >
                  <p className="text-[10px] font-semibold uppercase tracking-wider text-white/40">
                    {item.label}
                  </p>
                  <p className={cn("mt-3 text-3xl font-bold", item.color)}>
                    {item.value}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Recent alerts */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="rounded-xl border border-white/[0.08] bg-white/[0.02] backdrop-blur-sm"
          >
            <div className="px-6 py-4 border-b border-white/[0.06]">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-teal-400/60">
                Recent Alerts
              </h3>
            </div>
            {summary.recent_alerts.length === 0 ? (
              <div className="flex flex-col items-center gap-3 px-6 py-16 text-center">
                <Bell className="h-8 w-8 text-white/10" />
                <p className="text-sm text-white/30">
                  No alerts recorded yet. Run a health check or start
                  monitoring.
                </p>
              </div>
            ) : (
              <ul className="divide-y divide-white/[0.06]">
                {summary.recent_alerts.map((alert, i) => {
                  const Icon = ICON_MAP[alert.alert_type] ?? Info;
                  return (
                    <motion.li
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.4 + i * 0.05 }}
                      className="flex items-start gap-3 px-6 py-4 transition-colors hover:bg-white/[0.02]"
                    >
                      <Icon
                        className={cn(
                          "mt-0.5 h-5 w-5 shrink-0",
                          alert.alert_type === "CRITICAL" && "text-red-400",
                          alert.alert_type === "WARNING" && "text-amber-400",
                          alert.alert_type === "INFO" && "text-emerald-400",
                        )}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-white/80">
                          {alert.message}
                        </p>
                        <p className="mt-0.5 text-xs text-white/35">
                          {new Date(alert.timestamp).toLocaleString()} · Risk:{" "}
                          {alert.risk_level} (
                          {(alert.probability * 100).toFixed(1)}%)
                        </p>
                      </div>
                      <Badge
                        variant={
                          alert.alert_type === "CRITICAL"
                            ? "danger"
                            : alert.alert_type === "WARNING"
                              ? "warning"
                              : "success"
                        }
                        className="shrink-0"
                      >
                        {alert.alert_type}
                      </Badge>
                    </motion.li>
                  );
                })}
              </ul>
            )}
          </motion.div>
        </>
      ) : null}
    </>
  );
}
