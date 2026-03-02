"""
Configuration file for AI Health Monitor System
"""
import os
import secrets

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Model configuration
MODEL_PATH = os.path.join(_BASE_DIR, 'models', 'health_predictor.pkl')
SCALER_PATH = os.path.join(_BASE_DIR, 'models', 'scaler.pkl')

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

# Server configuration
HOST = '127.0.0.1'  # Localhost only for security
PORT = 5000
DEBUG = False  # Set to True only for development

# Data configuration
DATA_PATH = os.path.join(_BASE_DIR, 'data', 'health_data.csv')
DATASET_SIZE = 1000

# Database configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'health_monitor.db')

# JWT / Auth configuration
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', secrets.token_hex(32))
JWT_ACCESS_TOKEN_EXPIRES = 3600       # 1 hour
JWT_REFRESH_TOKEN_EXPIRES = 86400 * 7  # 7 days

# Rate limiting
RATE_LIMIT_DEFAULT = "60/minute"
RATE_LIMIT_AUTH = "10/minute"         # login / register
RATE_LIMIT_PREDICT = "30/minute"

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Roles
ROLES = ['patient', 'doctor', 'admin']
