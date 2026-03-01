"""
Anomaly Detection Module
Detects unusual vital sign patterns using Isolation Forest
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_PATH, HEALTH_PARAMS

ANOMALY_MODEL_PATH = 'models/anomaly_detector.pkl'
ANOMALY_SCALER_PATH = 'models/anomaly_scaler.pkl'

FEATURE_NAMES = [
    'heart_rate', 'blood_pressure_systolic',
    'blood_pressure_diastolic', 'temperature',
    'oxygen_saturation', 'respiratory_rate'
]


class AnomalyDetector:
    """Detects anomalous vital sign readings using Isolation Forest."""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.training_stats = None  # mean/std per feature for context

    def train(self, data_path=DATA_PATH):
        """Train the Isolation Forest on healthy-range data."""
        df = pd.read_csv(data_path)
        X = df[FEATURE_NAMES]

        # Store training distribution statistics
        self.training_stats = {
            col: {'mean': float(X[col].mean()), 'std': float(X[col].std())}
            for col in FEATURE_NAMES
        }

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model = IsolationForest(
            n_estimators=150,
            contamination=0.08,  # ~8 % expected anomalies
            max_samples='auto',
            random_state=42,
        )
        self.model.fit(X_scaled)

        # Evaluate on training set
        preds = self.model.predict(X_scaled)
        n_anomalies = (preds == -1).sum()
        print(f"Anomaly Detector trained — {n_anomalies}/{len(X)} flagged ({n_anomalies/len(X)*100:.1f}%)")

        self.save_model()
        return n_anomalies, len(X)

    def save_model(self):
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, ANOMALY_MODEL_PATH)
        joblib.dump({'scaler': self.scaler, 'stats': self.training_stats}, ANOMALY_SCALER_PATH)
        print(f"Anomaly model saved to {ANOMALY_MODEL_PATH}")

    def load_model(self):
        if os.path.exists(ANOMALY_MODEL_PATH) and os.path.exists(ANOMALY_SCALER_PATH):
            self.model = joblib.load(ANOMALY_MODEL_PATH)
            meta = joblib.load(ANOMALY_SCALER_PATH)
            self.scaler = meta['scaler']
            self.training_stats = meta['stats']
            return True
        return False

    def detect(self, vitals_dict):
        """
        Detect whether a single vitals reading is anomalous.

        Returns dict:
            is_anomaly: bool
            anomaly_score: float (lower = more anomalous, typically -1 to 0)
            deviations: dict per-feature z-score from training distribution
            flagged_vitals: list of features that individually deviate >2σ
        """
        if self.model is None or self.scaler is None:
            if not self.load_model():
                # Train on the fly if no saved model
                self.train()

        features = np.array([[vitals_dict[f] for f in FEATURE_NAMES]])
        features_scaled = self.scaler.transform(features)

        prediction = self.model.predict(features_scaled)[0]   # 1 = normal, -1 = anomaly
        score = self.model.decision_function(features_scaled)[0]  # continuous score

        # Per-feature deviation analysis
        deviations = {}
        flagged = []
        for i, fname in enumerate(FEATURE_NAMES):
            if self.training_stats:
                mean = self.training_stats[fname]['mean']
                std = self.training_stats[fname]['std']
                z = (vitals_dict[fname] - mean) / std if std > 0 else 0.0
                deviations[fname] = round(z, 2)
                if abs(z) > 2:
                    flagged.append(fname)

        return {
            'is_anomaly': bool(prediction == -1),
            'anomaly_score': round(float(score), 4),
            'deviations': deviations,
            'flagged_vitals': flagged,
        }

    def detect_batch(self, vitals_list):
        """Detect anomalies for a list of vitals dicts."""
        return [self.detect(v) for v in vitals_list]


if __name__ == '__main__':
    detector = AnomalyDetector()
    detector.train()

    # Test with healthy vs anomalous
    normal = {'heart_rate': 72, 'blood_pressure_systolic': 118,
              'blood_pressure_diastolic': 76, 'temperature': 36.6,
              'oxygen_saturation': 98, 'respiratory_rate': 16}
    anomalous = {'heart_rate': 180, 'blood_pressure_systolic': 200,
                 'blood_pressure_diastolic': 130, 'temperature': 40.5,
                 'oxygen_saturation': 72, 'respiratory_rate': 38}

    print("\nNormal vitals:", detector.detect(normal))
    print("Anomalous vitals:", detector.detect(anomalous))
