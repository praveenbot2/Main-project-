"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Save, Check, Settings, Server, Timer } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export default function SettingsPage() {
  const [apiUrl, setApiUrl] = useState(
    process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:5000",
  );
  const [refreshInterval, setRefreshInterval] = useState(3);
  const [saved, setSaved] = useState(false);

  function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8 flex items-center gap-3"
      >
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/[0.06] border border-white/[0.1]">
          <Settings className="h-5 w-5 text-white/60" />
        </div>
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Settings
          </h1>
          <p className="text-sm text-white/50">
            Configure API connection and monitoring preferences
          </p>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="max-w-xl"
      >
        <div className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-6 backdrop-blur-sm">
          <div className="mb-6">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-teal-400/60">
              Configuration
            </h2>
            <p className="mt-1 text-xs text-white/35">
              Manage your connection settings and monitoring preferences
            </p>
          </div>

          <form onSubmit={handleSave} className="space-y-6">
            {/* API URL */}
            <div>
              <label className="mb-1.5 flex items-center gap-2 text-sm font-medium text-white/70">
                <Server className="h-3.5 w-3.5 text-teal-400/50" />
                Backend API URL
              </label>
              <input
                type="url"
                value={apiUrl}
                onChange={(e) => setApiUrl(e.target.value)}
                className="w-full rounded-lg border border-white/[0.1] bg-white/[0.05] px-3 py-2.5 text-sm text-white placeholder:text-white/30 focus:border-teal-500/50 focus:outline-none focus:ring-1 focus:ring-teal-500/30 transition-colors"
              />
              <p className="mt-1 text-xs text-white/30">
                Flask server address (default: http://127.0.0.1:5000)
              </p>
            </div>

            {/* Refresh interval */}
            <div>
              <label className="mb-1.5 flex items-center gap-2 text-sm font-medium text-white/70">
                <Timer className="h-3.5 w-3.5 text-teal-400/50" />
                Live Monitor Refresh Interval (seconds)
              </label>
              <input
                type="number"
                min={1}
                max={60}
                value={refreshInterval}
                onChange={(e) => setRefreshInterval(Number(e.target.value))}
                className="w-full rounded-lg border border-white/[0.1] bg-white/[0.05] px-3 py-2.5 text-sm text-white placeholder:text-white/30 focus:border-teal-500/50 focus:outline-none focus:ring-1 focus:ring-teal-500/30 transition-colors"
              />
            </div>

            <div className="flex items-center gap-3 pt-2">
              <motion.button
                type="submit"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex items-center gap-2 rounded-xl px-6 py-3 text-sm font-semibold text-white transition-all"
                style={{
                  background:
                    "linear-gradient(135deg, #14B8A6 0%, #0D9488 100%)",
                  boxShadow: "0 4px 20px rgba(20,184,166,0.3)",
                }}
              >
                <Save className="h-4 w-4" />
                Save Settings
              </motion.button>

              {saved && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <Badge variant="success" className="gap-1">
                    <Check className="h-3 w-3" />
                    Saved
                  </Badge>
                </motion.div>
              )}
            </div>
          </form>
        </div>

        {/* Info card */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-6 rounded-xl border border-teal-500/10 bg-teal-500/[0.03] p-5"
        >
          <h3 className="text-xs font-semibold uppercase tracking-wider text-teal-400/50 mb-2">
            System Info
          </h3>
          <div className="space-y-1.5 text-xs text-white/35">
            <p>
              Version:{" "}
              <span className="text-white/60">AI Health Monitor v1.0</span>
            </p>
            <p>
              Frontend:{" "}
              <span className="text-white/60">Next.js 16 + Tailwind CSS</span>
            </p>
            <p>
              Backend:{" "}
              <span className="text-white/60">Flask + Scikit-learn</span>
            </p>
          </div>
        </motion.div>
      </motion.div>
    </>
  );
}
