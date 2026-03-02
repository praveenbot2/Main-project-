// ──────────────────────────────────────────────────────────────
// API client – talks to the backend via the /api prefix.
// In production (Vercel): /api/* → Python serverless function.
// In local dev: Next.js rewrites proxy /api/* → Flask on :5000.
// ──────────────────────────────────────────────────────────────

import type {
  Vitals,
  PredictResponse,
  ChatResponse,
  MonitorResponse,
  AlertSummaryResponse,
  HealthCheckResponse,
  Condition,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error((body as { error?: string }).error ?? res.statusText);
  }
  return res.json() as Promise<T>;
}

/** GET /api/health – backend health check */
export const getHealthCheck = () => request<HealthCheckResponse>("/api/health");

/** POST /api/predict – send vitals, receive risk prediction */
export const predictHealth = (vitals: Vitals) =>
  request<PredictResponse>("/api/predict", {
    method: "POST",
    body: JSON.stringify(vitals),
  });

/** POST /api/chat – send message to the health chatbot */
export const sendChat = (message: string) =>
  request<ChatResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify({ message }),
  });

/** GET /api/monitor?condition=... – get simulated vitals + prediction */
export const getMonitorData = (condition: Condition = "healthy") =>
  request<MonitorResponse>(`/api/monitor?condition=${condition}`);

/** GET /api/alerts – alert summary */
export const getAlerts = () => request<AlertSummaryResponse>("/api/alerts");

/** POST /api/simulate – run a simulated monitoring round */
export const simulateMonitoring = (condition: Condition = "healthy") =>
  request<{ success: boolean; monitoring_result: Record<string, unknown> }>(
    "/api/simulate",
    { method: "POST", body: JSON.stringify({ condition }) },
  );
