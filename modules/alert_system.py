"""
Alert System Module
Manages health alerts and notifications
"""

from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import ALERT_THRESHOLDS


class AlertSystem:
    """Manages health monitoring alerts"""
    
    def __init__(self):
        self.alert_history = []
    
    def check_and_alert(self, prediction_result, health_data):
        """
        Check prediction results and generate alerts if necessary
        
        Args:
            prediction_result: dict from HealthPredictor.predict()
            health_data: dict with vital signs
        
        Returns:
            dict with alert information
        """
        risk_level = prediction_result['risk_level']
        probability = prediction_result['probability']
        
        alert = {
            'timestamp': datetime.now().isoformat(),
            'risk_level': risk_level,
            'probability': probability,
            'vital_signs': health_data,
            'should_alert': False,
            'alert_type': None,
            'message': '',
            'recommendations': prediction_result['recommendations']
        }
        
        # Determine if alert should be triggered (case-insensitive comparison)
        rl = risk_level.lower() if isinstance(risk_level, str) else str(risk_level)
        if rl == 'high':
            alert['should_alert'] = True
            alert['alert_type'] = 'CRITICAL'
            alert['message'] = '🚨 CRITICAL: High health risk detected! Immediate medical attention required.'
        elif rl == 'medium':
            alert['should_alert'] = True
            alert['alert_type'] = 'WARNING'
            alert['message'] = '⚠️ WARNING: Moderate health risk detected. Please monitor closely and consult a doctor.'
        else:
            alert['alert_type'] = 'INFO'
            alert['message'] = '✓ INFO: Health parameters are normal. Keep up the good work!'
        
        # Add to history
        self.alert_history.append(alert)
        
        # Trigger notification if needed
        if alert['should_alert']:
            self._trigger_notification(alert)
        
        return alert
    
    def _trigger_notification(self, alert):
        """Trigger notification (can be extended to send emails, SMS, etc.)"""
        print(f"\n{'='*60}")
        print(f"ALERT TRIGGERED: {alert['alert_type']}")
        print(f"Time: {alert['timestamp']}")
        print(f"Message: {alert['message']}")
        print(f"Risk Level: {alert['risk_level']} (Probability: {alert['probability']})")
        print(f"{'='*60}\n")
    
    def get_alert_summary(self):
        """Get summary of all alerts"""
        if not self.alert_history:
            return "No alerts in history"
        
        total_alerts = len(self.alert_history)
        critical = sum(1 for a in self.alert_history if a['alert_type'] == 'CRITICAL')
        warning = sum(1 for a in self.alert_history if a['alert_type'] == 'WARNING')
        info = sum(1 for a in self.alert_history if a['alert_type'] == 'INFO')
        
        return {
            'total_alerts': total_alerts,
            'critical': critical,
            'warning': warning,
            'info': info,
            'recent_alerts': self.alert_history[-5:]  # Last 5 alerts
        }
    
    def clear_history(self):
        """Clear alert history"""
        self.alert_history = []
        print("Alert history cleared")


if __name__ == "__main__":
    # Test the alert system
    alert_system = AlertSystem()
    
    # Test case 1: Normal vitals
    test_data1 = {
        'heart_rate': 75,
        'blood_pressure_systolic': 120,
        'blood_pressure_diastolic': 80,
        'temperature': 36.8,
        'oxygen_saturation': 98,
        'respiratory_rate': 16
    }
    
    test_result1 = {
        'risk_level': 'low',
        'probability': 0.85,
        'recommendations': ['Keep up good health']
    }
    
    print("Test 1: Normal vitals")
    alert1 = alert_system.check_and_alert(test_result1, test_data1)
    print(f"Alert type: {alert1['alert_type']}")
    print(f"Should alert: {alert1['should_alert']}")
    print()
    
    # Test case 2: High risk
    test_data2 = {
        'heart_rate': 150,
        'blood_pressure_systolic': 180,
        'blood_pressure_diastolic': 110,
        'temperature': 39.0,
        'oxygen_saturation': 85,
        'respiratory_rate': 30
    }
    
    test_result2 = {
        'risk_level': 'high',
        'probability': 0.92,
        'recommendations': ['Seek immediate medical attention']
    }
    
    print("Test 2: High risk vitals")
    alert2 = alert_system.check_and_alert(test_result2, test_data2)
    print(f"Alert type: {alert2['alert_type']}")
    print(f"Should alert: {alert2['should_alert']}")
    print()
    
    # Get summary
    print("Alert Summary:")
    summary = alert_system.get_alert_summary()
    print(summary)
