"""
Configuration file for AI Health Monitor System
"""
import os

# Model configuration
MODEL_PATH = 'models/health_predictor.pkl'
SCALER_PATH = 'models/scaler.pkl'

# Alert thresholds
ALERT_THRESHOLDS = {
    'high_risk': 0.7,
    'medium_risk': 0.4,
    'low_risk': 0.2
}

# Health parameters ranges
HEALTH_PARAMS = {
    'heart_rate': {'min': 40, 'max': 200, 'normal': (60, 100)},
    'blood_pressure_systolic': {'min': 70, 'max': 200, 'normal': (90, 120)},
    'blood_pressure_diastolic': {'min': 40, 'max': 130, 'normal': (60, 80)},
    'temperature': {'min': 35.0, 'max': 42.0, 'normal': (36.1, 37.2)},
    'oxygen_saturation': {'min': 70, 'max': 100, 'normal': (95, 100)},
    'respiratory_rate': {'min': 8, 'max': 40, 'normal': (12, 20)}
}

# Data configuration
DATA_PATH = 'data/health_data.csv'
DATASET_SIZE = 1000
