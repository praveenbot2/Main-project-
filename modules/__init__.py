"""
AI Health Monitor - Modules Package
"""

__version__ = "3.0.0"
__author__ = "AI Health Monitor Team"

from .data_generator import DataGenerator
from .ai_predictor import HealthPredictor
from .alert_system import AlertSystem
from .chatbot import HealthChatbot
from .real_time_monitor import RealTimeMonitor
from .anomaly_detector import AnomalyDetector
from .forecaster import VitalForecaster
from .smart_chatbot import SmartChatbot

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
