"""
Real-time Monitoring Module
Continuously monitors health vitals and triggers alerts
"""

import time
import numpy as np
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.ai_predictor import HealthPredictor
from modules.alert_system import AlertSystem
from config import HEALTH_PARAMS


class RealTimeMonitor:
    """Real-time health monitoring system"""
    
    def __init__(self, predictor=None, alert_system=None):
        self.predictor = predictor or HealthPredictor()
        self.alert_system = alert_system or AlertSystem()
        self.is_monitoring = False
        self.monitoring_history = []
    
    def initialize(self):
        """Initialize the monitoring system"""
        print("Initializing Real-Time Health Monitor...")
        success = self.predictor.load_model()
        if success:
            print("✓ AI Model loaded successfully")
            print("✓ Alert System initialized")
            print("✓ Real-Time Monitor ready")
            return True
        else:
            print("✗ Failed to load AI model. Please train the model first.")
            return False
    
    def simulate_vitals(self, base_condition='healthy'):
        """
        Simulate real-time vital signs (for demo purposes)
        In production, this would read from actual sensors
        
        Args:
            base_condition: 'healthy', 'at_risk', or 'critical'
        
        Returns:
            dict with simulated vital signs
        """
        if base_condition == 'healthy':
            vitals = {
                'heart_rate': np.random.normal(75, 5),
                'blood_pressure_systolic': np.random.normal(115, 5),
                'blood_pressure_diastolic': np.random.normal(75, 3),
                'temperature': np.random.normal(36.6, 0.2),
                'oxygen_saturation': np.random.normal(98, 1),
                'respiratory_rate': np.random.normal(16, 1)
            }
        elif base_condition == 'at_risk':
            vitals = {
                'heart_rate': np.random.normal(110, 10),
                'blood_pressure_systolic': np.random.normal(145, 8),
                'blood_pressure_diastolic': np.random.normal(92, 5),
                'temperature': np.random.normal(37.5, 0.3),
                'oxygen_saturation': np.random.normal(93, 2),
                'respiratory_rate': np.random.normal(22, 2)
            }
        else:  # critical
            vitals = {
                'heart_rate': np.random.normal(140, 15),
                'blood_pressure_systolic': np.random.normal(170, 10),
                'blood_pressure_diastolic': np.random.normal(105, 8),
                'temperature': np.random.normal(38.5, 0.5),
                'oxygen_saturation': np.random.normal(88, 2),
                'respiratory_rate': np.random.normal(28, 3)
            }
        
        # Apply realistic constraints
        vitals['heart_rate'] = np.clip(vitals['heart_rate'], 40, 200)
        vitals['blood_pressure_systolic'] = np.clip(vitals['blood_pressure_systolic'], 70, 200)
        vitals['blood_pressure_diastolic'] = np.clip(vitals['blood_pressure_diastolic'], 40, 130)
        vitals['temperature'] = np.clip(vitals['temperature'], 35.0, 42.0)
        vitals['oxygen_saturation'] = np.clip(vitals['oxygen_saturation'], 70, 100)
        vitals['respiratory_rate'] = np.clip(vitals['respiratory_rate'], 8, 40)
        
        # Round values
        return {k: round(v, 1) for k, v in vitals.items()}
    
    def monitor_once(self, vitals):
        """
        Perform a single monitoring check
        
        Args:
            vitals: dict with health vital signs
        
        Returns:
            dict with monitoring results
        """
        timestamp = datetime.now()
        
        # Get AI prediction
        prediction = self.predictor.predict(vitals)
        
        # Check and generate alerts
        alert = self.alert_system.check_and_alert(prediction, vitals)
        
        # Store in history
        monitoring_record = {
            'timestamp': timestamp.isoformat(),
            'vitals': vitals,
            'prediction': prediction,
            'alert': alert
        }
        self.monitoring_history.append(monitoring_record)
        
        return monitoring_record
    
    def continuous_monitor(self, duration_seconds=60, interval_seconds=5, 
                          condition='healthy'):
        """
        Continuously monitor health vitals
        
        Args:
            duration_seconds: Total monitoring duration
            interval_seconds: Time between each check
            condition: Simulated health condition
        """
        if not self.initialize():
            return
        
        self.is_monitoring = True
        print(f"\n{'='*70}")
        print(f"Starting Real-Time Health Monitoring")
        print(f"Duration: {duration_seconds} seconds | Interval: {interval_seconds} seconds")
        print(f"Simulated Condition: {condition}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        check_count = 0
        
        try:
            while self.is_monitoring and (time.time() - start_time) < duration_seconds:
                check_count += 1
                
                # Simulate or read vitals
                vitals = self.simulate_vitals(condition)
                
                # Perform monitoring check
                print(f"\n--- Check #{check_count} at {datetime.now().strftime('%H:%M:%S')} ---")
                print(f"Vitals: HR={vitals['heart_rate']} bpm, "
                      f"BP={vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} mmHg, "
                      f"Temp={vitals['temperature']}°C, "
                      f"SpO2={vitals['oxygen_saturation']}%, "
                      f"RR={vitals['respiratory_rate']} /min")
                
                result = self.monitor_once(vitals)
                
                print(f"Risk Assessment: {result['prediction']['risk_level'].upper()} "
                      f"(Confidence: {result['prediction']['probability']})")
                print(f"Alert Status: {result['alert']['alert_type']}")
                
                # Wait for next check
                time.sleep(interval_seconds)
        
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
        
        finally:
            self.is_monitoring = False
            print(f"\n{'='*70}")
            print(f"Monitoring Session Complete")
            print(f"Total Checks: {check_count}")
            print(f"Duration: {time.time() - start_time:.1f} seconds")
            self._print_session_summary()
            print(f"{'='*70}\n")
    
    def _print_session_summary(self):
        """Print summary of monitoring session"""
        if not self.monitoring_history:
            return
        
        summary = self.alert_system.get_alert_summary()
        print(f"\nSession Summary:")
        print(f"  Critical Alerts: {summary['critical_alerts']}")
        print(f"  Warning Alerts: {summary['warning_alerts']}")
        print(f"  Info Messages: {summary['info_alerts']}")
    
    def get_history(self, last_n=10):
        """Get last N monitoring records"""
        return self.monitoring_history[-last_n:]
    
    def clear_history(self):
        """Clear monitoring history"""
        self.monitoring_history = []
        self.alert_system.clear_history()
        print("Monitoring history cleared")


if __name__ == "__main__":
    monitor = RealTimeMonitor()
    
    # Run a short monitoring session
    print("Starting demo monitoring session...")
    print("Testing with healthy vitals for 30 seconds...\n")
    monitor.continuous_monitor(duration_seconds=30, interval_seconds=5, 
                              condition='healthy')
