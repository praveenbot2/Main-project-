"""
Time-Series Forecasting Module
Predicts future vital sign trends using statistical methods
"""

import numpy as np
from datetime import datetime, timedelta
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HEALTH_PARAMS

VITAL_NAMES = [
    'heart_rate', 'blood_pressure_systolic',
    'blood_pressure_diastolic', 'temperature',
    'oxygen_saturation', 'respiratory_rate'
]


class VitalForecaster:
    """Forecasts future vital sign trends from historical readings."""

    def __init__(self, min_points=5):
        self.min_points = min_points

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def forecast(self, history, horizons_hours=None):
        """
        Forecast future vital values.

        Args:
            history: list of dicts, each with vital keys + 'created_at' ISO timestamp.
                     Must be ordered oldest-first.
            horizons_hours: list of forecast horizons in hours (default [1, 6, 24])

        Returns:
            dict keyed by vital name, each containing:
                trend: 'rising' | 'falling' | 'stable'
                slope: float (units per hour)
                current_avg: float (recent average)
                forecasts: list of {horizon_h, predicted_value, confidence_low, confidence_high}
                warning: str | None
        """
        if horizons_hours is None:
            horizons_hours = [1, 6, 24]

        if len(history) < self.min_points:
            return {'error': f'Need at least {self.min_points} data points, got {len(history)}'}

        # Parse timestamps to hours-since-first
        t0 = self._parse_ts(history[0].get('created_at', ''))
        times_h = []
        for row in history:
            ts = self._parse_ts(row.get('created_at', ''))
            times_h.append((ts - t0).total_seconds() / 3600.0)

        results = {}
        for vital in VITAL_NAMES:
            values = [float(row.get(vital, 0)) for row in history]
            results[vital] = self._forecast_single(
                times_h, values, horizons_hours, vital
            )

        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _forecast_single(self, times, values, horizons, vital_name):
        """Forecast a single vital using exponential smoothing + linear trend."""
        t = np.array(times, dtype=float)
        v = np.array(values, dtype=float)

        # --- Exponential smoothing (Holt's linear trend method) ---
        alpha = 0.4  # level smoothing
        beta = 0.2   # trend smoothing

        level = v[0]
        trend = 0.0
        if len(v) > 1:
            trend = (v[-1] - v[0]) / max(t[-1] - t[0], 0.01)

        for i in range(1, len(v)):
            dt = t[i] - t[i - 1] if i > 0 else 1.0
            dt = max(dt, 0.001)
            prev_level = level
            level = alpha * v[i] + (1 - alpha) * (level + trend * dt)
            trend = beta * ((level - prev_level) / dt) + (1 - beta) * trend

        # Residual std for confidence interval
        fitted = self._holt_fitted(t, v, alpha, beta)
        residuals = v - fitted
        std_err = float(np.std(residuals)) if len(residuals) > 1 else 0.0

        # Current average (last 5 readings)
        recent_n = min(5, len(v))
        current_avg = float(np.mean(v[-recent_n:]))

        # Slope (units per hour from trend component)
        slope = float(trend)

        # Classify trend
        normal_range = HEALTH_PARAMS.get(vital_name, {}).get('normal', (0, 1))
        range_span = normal_range[1] - normal_range[0]
        threshold = range_span * 0.02  # 2 % of normal range per hour
        if abs(slope) < threshold:
            trend_dir = 'stable'
        elif slope > 0:
            trend_dir = 'rising'
        else:
            trend_dir = 'falling'

        # Forecasts
        last_t = t[-1]
        forecasts = []
        for h in horizons:
            pred = level + trend * h
            # Wider confidence band for longer horizons
            ci = 1.96 * std_err * np.sqrt(1 + h / max(last_t, 1))
            forecasts.append({
                'horizon_h': h,
                'predicted_value': round(float(pred), 2),
                'confidence_low': round(float(pred - ci), 2),
                'confidence_high': round(float(pred + ci), 2),
            })

        # Warning if forecast leaves normal range
        warning = None
        limits = HEALTH_PARAMS.get(vital_name, {})
        for fc in forecasts:
            lo, hi = limits.get('normal', (None, None))
            if lo is not None and fc['predicted_value'] < lo:
                warning = f'{vital_name} may drop below normal ({lo}) in ~{fc["horizon_h"]}h'
                break
            if hi is not None and fc['predicted_value'] > hi:
                warning = f'{vital_name} may rise above normal ({hi}) in ~{fc["horizon_h"]}h'
                break

        return {
            'trend': trend_dir,
            'slope': round(slope, 4),
            'current_avg': round(current_avg, 2),
            'forecasts': forecasts,
            'warning': warning,
        }

    @staticmethod
    def _holt_fitted(t, v, alpha, beta):
        """Return fitted values from Holt's linear trend smoothing."""
        fitted = np.zeros_like(v, dtype=float)
        level = v[0]
        trend = 0.0
        if len(v) > 1:
            trend = (v[-1] - v[0]) / max(t[-1] - t[0], 0.01)

        fitted[0] = level
        for i in range(1, len(v)):
            dt = t[i] - t[i - 1]
            dt = max(dt, 0.001)
            prev_level = level
            level = alpha * v[i] + (1 - alpha) * (level + trend * dt)
            trend = beta * ((level - prev_level) / dt) + (1 - beta) * trend
            fitted[i] = level
        return fitted

    @staticmethod
    def _parse_ts(ts_str):
        """Parse an ISO-format timestamp string."""
        if not ts_str:
            return datetime.now()
        # Handle SQLite datetime format (no T)
        ts_str = ts_str.replace('T', ' ').split('.')[0]
        try:
            return datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.now()
