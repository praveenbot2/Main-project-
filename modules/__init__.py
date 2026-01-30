"""
AI Health Monitor - Modules Package
"""

__version__ = "1.0.0"
__author__ = "AI Health Monitor Team"

from .data_generator import DataGenerator
from .ai_predictor import HealthPredictor
from .alert_system import AlertSystem
from .chatbot import HealthChatbot
from .real_time_monitor import RealTimeMonitor

__all__ = [
    'DataGenerator',
    'HealthPredictor',
    'AlertSystem',
    'HealthChatbot',
    'RealTimeMonitor'
]
