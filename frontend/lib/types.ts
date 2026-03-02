// ──────────────────────────────────────────────────────────────
// Shared TypeScript types for the AI Health Monitor frontend
// ──────────────────────────────────────────────────────────────

export interface Vitals {
  heart_rate: number;
  blood_pressure_systolic: number;
  blood_pressure_diastolic: number;
  temperature: number;
  oxygen_saturation: number;
  respiratory_rate: number;
}

export interface Prediction {
  risk_level: "Low" | "Medium" | "High";
  probability: number;
  recommendations: string[];
  details?: Record<string, unknown>;
}

export interface Alert {
  timestamp: string;
  risk_level: string;
  probability: number;
  vital_signs: Vitals;
  should_alert: boolean;
  alert_type: "CRITICAL" | "WARNING" | "INFO";
  message: string;
  recommendations: string[];
}

export interface PredictResponse {
  success: boolean;
  vitals: Vitals;
  prediction: Prediction;
  alert: Alert;
}

export interface ChatResponse {
  success: boolean;
  user_message: string;
  bot_response: string;
  conversation_history: { role: string; content: string }[];
}

export interface MonitorResponse {
  success: boolean;
  timestamp: string;
  vitals: Vitals;
  prediction: Prediction;
}

export interface AlertSummaryResponse {
  success: boolean;
  alerts: {
    total_alerts: number;
    critical_alerts: number;
    warning_alerts: number;
    info_alerts: number;
    recent_alerts: Alert[];
  };
}

export interface HealthCheckResponse {
  status: string;
  model_loaded: boolean;
}

export type RiskLevel = "Low" | "Medium" | "High";
export type Condition = "healthy" | "at_risk" | "critical";
