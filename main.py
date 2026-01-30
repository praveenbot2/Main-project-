"""
Main Application
AI-Driven Health Monitoring and Alert System
"""

import sys
import os

# Add modules directory to path
sys.path.insert(0, os.path.dirname(__file__))

from modules.data_generator import DataGenerator
from modules.ai_predictor import HealthPredictor
from modules.alert_system import AlertSystem
from modules.chatbot import HealthChatbot
from modules.real_time_monitor import RealTimeMonitor


class HealthMonitorApp:
    """Main application class for AI Health Monitor"""
    
    def __init__(self):
        self.data_generator = DataGenerator()
        self.predictor = HealthPredictor()
        self.alert_system = AlertSystem()
        self.chatbot = HealthChatbot()
        self.monitor = RealTimeMonitor()
    
    def setup(self):
        """Setup the system - generate data and train model"""
        print("\n" + "="*70)
        print("AI-Driven Health Monitoring and Alert System - Setup")
        print("="*70 + "\n")
        
        # Step 1: Generate dataset
        print("Step 1: Generating health monitoring dataset...")
        self.data_generator.save_dataset()
        print()
        
        # Step 2: Train AI model
        print("Step 2: Training AI prediction model...")
        self.predictor.train()
        print()
        
        print("✓ Setup completed successfully!\n")
    
    def predict_health(self, vitals):
        """Predict health risk for given vitals"""
        prediction = self.predictor.predict(vitals)
        alert = self.alert_system.check_and_alert(prediction, vitals)
        
        return {
            'vitals': vitals,
            'prediction': prediction,
            'alert': alert
        }
    
    def start_monitoring(self, duration=60, interval=5, condition='healthy'):
        """Start real-time monitoring"""
        self.monitor.continuous_monitor(duration, interval, condition)
    
    def chat(self, message):
        """Chat with health assistant"""
        return self.chatbot.process_message(message)
    
    def interactive_demo(self):
        """Run interactive demo"""
        print("\n" + "="*70)
        print("AI Health Monitor - Interactive Demo")
        print("="*70 + "\n")
        
        print("Choose a mode:")
        print("1. Single Health Check")
        print("2. Real-Time Monitoring")
        print("3. Chat with Health Assistant")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            self._demo_single_check()
        elif choice == '2':
            self._demo_real_time()
        elif choice == '3':
            self._demo_chatbot()
        elif choice == '4':
            print("Goodbye!")
            return
        else:
            print("Invalid choice")
    
    def _demo_single_check(self):
        """Demo single health check"""
        print("\n--- Single Health Check ---")
        print("Enter your vital signs:")
        
        try:
            vitals = {
                'heart_rate': float(input("Heart Rate (bpm): ")),
                'blood_pressure_systolic': float(input("Blood Pressure Systolic (mmHg): ")),
                'blood_pressure_diastolic': float(input("Blood Pressure Diastolic (mmHg): ")),
                'temperature': float(input("Body Temperature (°C): ")),
                'oxygen_saturation': float(input("Oxygen Saturation (%): ")),
                'respiratory_rate': float(input("Respiratory Rate (/min): "))
            }
            
            result = self.predict_health(vitals)
            
            print("\n--- Health Assessment Result ---")
            print(f"Risk Level: {result['prediction']['risk_level'].upper()}")
            print(f"Confidence: {result['prediction']['probability']}")
            print(f"\nRecommendations:")
            for rec in result['prediction']['recommendations']:
                print(f"  {rec}")
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        except Exception as e:
            print(f"Error: {e}")
    
    def _demo_real_time(self):
        """Demo real-time monitoring"""
        print("\n--- Real-Time Monitoring Demo ---")
        print("Select simulation condition:")
        print("1. Healthy")
        print("2. At Risk")
        print("3. Critical")
        
        condition_map = {'1': 'healthy', '2': 'at_risk', '3': 'critical'}
        choice = input("Enter choice (1-3): ").strip()
        condition = condition_map.get(choice, 'healthy')
        
        duration = int(input("Monitoring duration (seconds, default 30): ") or "30")
        interval = int(input("Check interval (seconds, default 5): ") or "5")
        
        self.start_monitoring(duration, interval, condition)
    
    def _demo_chatbot(self):
        """Demo chatbot"""
        print("\n--- Health Assistant Chatbot ---")
        print("Type 'exit' to return to main menu\n")
        
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
            
            response = self.chat(user_input)
            print(f"\nAssistant: {response}\n")


def main():
    """Main entry point"""
    app = HealthMonitorApp()
    
    # Check if setup is needed
    if not os.path.exists('models/health_predictor.pkl'):
        print("First-time setup required...")
        app.setup()
    else:
        # Load existing model
        app.predictor.load_model()
    
    # Run interactive demo
    while True:
        app.interactive_demo()
        
        continue_choice = input("\nWould you like to try another mode? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\nThank you for using AI Health Monitor!")
            break


if __name__ == "__main__":
    main()
