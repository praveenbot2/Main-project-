"""
AI Prediction Module
Trains and predicts health risk using machine learning
Supports feature engineering, ensemble methods, and model versioning
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    VotingClassifier,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
import joblib
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MODEL_PATH, SCALER_PATH, DATA_PATH, ALERT_THRESHOLDS


class HealthPredictor:
    """AI model for health risk prediction with ensemble and feature engineering"""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.training_metrics = None
        self.raw_feature_names = [
            'heart_rate', 'blood_pressure_systolic',
            'blood_pressure_diastolic', 'temperature',
            'oxygen_saturation', 'respiratory_rate'
        ]
        # Derived features added by feature engineering
        self.derived_feature_names = [
            'pulse_pressure',       # systolic - diastolic
            'mean_arterial_pressure',  # diastolic + (systolic - diastolic)/3
            'temp_deviation',       # abs(temp - 37.0)
            'o2_deficit',           # 100 - o2_saturation
        ]
        # For backward compat, predict() still accepts the 6 raw vitals
        self.feature_names = self.raw_feature_names

    @staticmethod
    def _derive_features(df_or_row):
        """Add derived features to a DataFrame or single-row array."""
        if isinstance(df_or_row, pd.DataFrame):
            df = df_or_row.copy()
            df['pulse_pressure'] = df['blood_pressure_systolic'] - df['blood_pressure_diastolic']
            df['mean_arterial_pressure'] = (
                df['blood_pressure_diastolic']
                + (df['blood_pressure_systolic'] - df['blood_pressure_diastolic']) / 3
            )
            df['temp_deviation'] = (df['temperature'] - 37.0).abs()
            df['o2_deficit'] = 100.0 - df['oxygen_saturation']
            return df
        # numpy array (1, 6) — single sample
        arr = np.array(df_or_row, dtype=float).reshape(1, -1)
        sys_, dia_ = arr[0, 1], arr[0, 2]
        temp_ = arr[0, 3]
        o2_ = arr[0, 4]
        derived = np.array([[
            sys_ - dia_,                         # pulse_pressure
            dia_ + (sys_ - dia_) / 3,            # MAP
            abs(temp_ - 37.0),                   # temp_deviation
            100.0 - o2_,                         # o2_deficit
        ]])
        return np.hstack([arr, derived])

    def prepare_data(self, df):
        """Prepare data for training (with derived features)"""
        X = df[self.raw_feature_names].copy()
        X = self._derive_features(X)
        all_features = self.raw_feature_names + self.derived_feature_names
        X = X[all_features]

        # Convert continuous risk_score to categories
        y = pd.cut(df['risk_score'],
                   bins=[-0.001, 0.3, 0.7, 1.001],
                   labels=['low', 'medium', 'high'])

        return X, y

    def train(self, data_path=DATA_PATH):
        """Train the health risk prediction ensemble model"""
        # Load data
        df = pd.read_csv(data_path)
        X, y = self.prepare_data(df)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Build ensemble: Random Forest + Gradient Boosting
        rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced',
        )
        gb = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
        )
        self.model = VotingClassifier(
            estimators=[('rf', rf), ('gb', gb)],
            voting='soft',
        )
        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average='weighted', zero_division=0
        )

        self.training_metrics = {
            'accuracy': round(float(accuracy), 4),
            'precision': round(float(precision), 4),
            'recall': round(float(recall), 4),
            'f1_score': round(float(f1), 4),
            'n_train': len(X_train),
            'n_test': len(X_test),
            'features': self.raw_feature_names + self.derived_feature_names,
        }

        print(f"Ensemble model trained successfully!")
        print(f"Accuracy: {accuracy:.3f}  |  Precision: {precision:.3f}  |  Recall: {recall:.3f}  |  F1: {f1:.3f}")
        print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

        # Save model and scaler
        self.save_model()

        return accuracy
    
    def save_model(self):
        """Save trained model, scaler, and metrics"""
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump({
            'scaler': self.scaler,
            'metrics': self.training_metrics,
        }, SCALER_PATH)
        print(f"Model saved to {MODEL_PATH}")
        print(f"Scaler saved to {SCALER_PATH}")

    def load_model(self):
        """Load trained model, scaler, and metrics"""
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            self.model = joblib.load(MODEL_PATH)
            meta = joblib.load(SCALER_PATH)
            # Support both old (plain scaler) and new (dict with scaler + metrics)
            if isinstance(meta, dict) and 'scaler' in meta:
                self.scaler = meta['scaler']
                self.training_metrics = meta.get('metrics')
            else:
                self.scaler = meta
                self.training_metrics = None
            print("Model loaded successfully")
            return True
        else:
            print("Model files not found. Please train the model first.")
            return False

    def get_metrics(self):
        """Return training metrics for the current model."""
        return self.training_metrics
    
    def predict(self, health_data):
        """
        Predict health risk for given vital signs
        
        Args:
            health_data: dict with keys matching feature_names
        
        Returns:
            dict with risk_level, probability, and recommendations
        """
        if self.model is None or self.scaler is None:
            if not self.load_model():
                raise ValueError("Model not loaded. Train the model first.")
        
        # Prepare input (raw 6 features)
        raw = np.array([[
            health_data['heart_rate'],
            health_data['blood_pressure_systolic'],
            health_data['blood_pressure_diastolic'],
            health_data['temperature'],
            health_data['oxygen_saturation'],
            health_data['respiratory_rate']
        ]])

        # Add derived features
        features = self._derive_features(raw)
        
        # Scale and predict
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Get class probabilities
        risk_prob = dict(zip(self.model.classes_, probabilities))
        max_prob = max(probabilities)
        
        # Capitalize risk level for frontend consistency
        capitalized = prediction.capitalize() if isinstance(prediction, str) else str(prediction)

        # Determine specific condition flags
        conditions = self._detect_conditions(health_data)

        return {
            'risk_level': capitalized,
            'probability': round(max_prob, 3),
            'risk_probabilities': {k: round(v, 3) for k, v in risk_prob.items()},
            'conditions': conditions,
            'recommendations': self._get_recommendations(prediction, health_data)
        }
    
    @staticmethod
    def _detect_conditions(health_data):
        """Detect specific health conditions from vital signs."""
        conditions = []
        hr = health_data.get('heart_rate', 0)
        sys = health_data.get('blood_pressure_systolic', 0)
        dia = health_data.get('blood_pressure_diastolic', 0)
        temp = health_data.get('temperature', 0)
        spo2 = health_data.get('oxygen_saturation', 100)
        rr = health_data.get('respiratory_rate', 0)

        if hr > 100:
            conditions.append({'name': 'tachycardia', 'severity': 'warning', 'detail': f'Heart rate {hr} bpm (>100)'})
        elif hr < 60:
            conditions.append({'name': 'bradycardia', 'severity': 'warning', 'detail': f'Heart rate {hr} bpm (<60)'})

        if sys >= 180 or dia >= 120:
            conditions.append({'name': 'hypertensive_crisis', 'severity': 'critical', 'detail': f'BP {sys}/{dia} mmHg'})
        elif sys >= 140 or dia >= 90:
            conditions.append({'name': 'hypertension', 'severity': 'warning', 'detail': f'BP {sys}/{dia} mmHg'})
        elif sys < 90 or dia < 60:
            conditions.append({'name': 'hypotension', 'severity': 'warning', 'detail': f'BP {sys}/{dia} mmHg'})

        if temp >= 38.0:
            label = 'high_fever' if temp >= 39.5 else 'fever'
            sev = 'critical' if temp >= 39.5 else 'warning'
            conditions.append({'name': label, 'severity': sev, 'detail': f'Temperature {temp}°C'})
        elif temp < 35.0:
            conditions.append({'name': 'hypothermia', 'severity': 'critical', 'detail': f'Temperature {temp}°C'})

        if spo2 < 90:
            conditions.append({'name': 'severe_hypoxemia', 'severity': 'critical', 'detail': f'SpO2 {spo2}%'})
        elif spo2 < 95:
            conditions.append({'name': 'hypoxemia', 'severity': 'warning', 'detail': f'SpO2 {spo2}%'})

        if rr > 20:
            conditions.append({'name': 'tachypnea', 'severity': 'warning', 'detail': f'RR {rr}/min (>20)'})
        elif rr < 12:
            conditions.append({'name': 'bradypnea', 'severity': 'warning', 'detail': f'RR {rr}/min (<12)'})

        return conditions

    def _get_recommendations(self, risk_level, health_data):
        """Generate health recommendations based on risk level"""
        recommendations = []
        
        rl = risk_level.lower() if isinstance(risk_level, str) else str(risk_level)
        if rl == 'high':
            recommendations.append("⚠️ URGENT: Seek immediate medical attention")
            recommendations.append("Contact emergency services if symptoms worsen")
        elif rl == 'medium':
            recommendations.append("⚠️ WARNING: Schedule a doctor's appointment soon")
            recommendations.append("Monitor your vital signs closely")
        else:
            recommendations.append("✓ Your health parameters are within normal range")
            recommendations.append("Continue maintaining a healthy lifestyle")
        
        # Specific recommendations
        if health_data['heart_rate'] > 100:
            recommendations.append("• Heart rate is elevated - consider rest and relaxation")
        elif health_data['heart_rate'] < 60:
            recommendations.append("• Heart rate is low - consult with a doctor")
        
        if health_data['blood_pressure_systolic'] > 130:
            recommendations.append("• Blood pressure is high - reduce salt intake")
        
        if health_data['oxygen_saturation'] < 95:
            recommendations.append("• Oxygen saturation is low - ensure proper breathing")
        
        if health_data['temperature'] > 37.5:
            recommendations.append("• Temperature is elevated - stay hydrated and rest")
        
        return recommendations


if __name__ == "__main__":
    predictor = HealthPredictor()
    predictor.train()
