"""
AI Health Monitor - Modules Package
"""

__version__ = "3.0.0"
__author__ = "AI Health Monitor Team"

# Core modules (always available)
from .ai_predictor import HealthPredictor
from .alert_system import AlertSystem
from .chatbot import HealthChatbot
from .real_time_monitor import RealTimeMonitor
from .smart_chatbot import SmartChatbot

# Optional modules (require pandas; not needed at API runtime)
try:
    from .data_generator import DataGenerator
except ImportError:
    DataGenerator = None  # type: ignore

try:
    from .anomaly_detector import AnomalyDetector
except ImportError:
    AnomalyDetector = None  # type: ignore

try:
    from .forecaster import VitalForecaster
except ImportError:
    VitalForecaster = None  # type: ignore

__all__ = [
    'DataGenerator',
    'HealthPredictor',
    'AlertSystem',
    'HealthChatbot',
    'RealTimeMonitor',
    'AnomalyDetector',
    'VitalForecaster',
    'SmartChatbot',
]
