"""
AI Prediction Module
Trains and predicts health risk using machine learning
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MODEL_PATH, SCALER_PATH, DATA_PATH, ALERT_THRESHOLDS


class HealthPredictor:
    """AI model for health risk prediction"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = [
            'heart_rate', 'blood_pressure_systolic', 
            'blood_pressure_diastolic', 'temperature', 
            'oxygen_saturation', 'respiratory_rate'
        ]
    
    def prepare_data(self, df):
        """Prepare data for training"""
        X = df[self.feature_names]
        
        # Convert continuous risk_score to categories
        y = pd.cut(df['risk_score'], 
                   bins=[-0.001, 0.3, 0.7, 1.001], 
                   labels=['low', 'medium', 'high'])
        
        return X, y
    
    def train(self, data_path=DATA_PATH):
        """Train the health risk prediction model"""
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
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100, 
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model trained successfully!")
        print(f"Accuracy: {accuracy:.3f}")
        print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
        
        # Save model and scaler
        self.save_model()
        
        return accuracy
    
    def save_model(self):
        """Save trained model and scaler"""
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.scaler, SCALER_PATH)
        print(f"Model saved to {MODEL_PATH}")
        print(f"Scaler saved to {SCALER_PATH}")
    
    def load_model(self):
        """Load trained model and scaler"""
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.scaler = joblib.load(SCALER_PATH)
            print("Model loaded successfully")
            return True
        else:
            print("Model files not found. Please train the model first.")
            return False
    
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
        
        # Prepare input
        features = np.array([[
            health_data['heart_rate'],
            health_data['blood_pressure_systolic'],
            health_data['blood_pressure_diastolic'],
            health_data['temperature'],
            health_data['oxygen_saturation'],
            health_data['respiratory_rate']
        ]])
        
        # Scale and predict
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Get class probabilities
        risk_prob = dict(zip(self.model.classes_, probabilities))
        max_prob = max(probabilities)
        
        return {
            'risk_level': prediction,
            'probability': round(max_prob, 3),
            'risk_probabilities': {k: round(v, 3) for k, v in risk_prob.items()},
            'recommendations': self._get_recommendations(prediction, health_data)
        }
    
    def _get_recommendations(self, risk_level, health_data):
        """Generate health recommendations based on risk level"""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.append("⚠️ URGENT: Seek immediate medical attention")
            recommendations.append("Contact emergency services if symptoms worsen")
        elif risk_level == 'medium':
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
