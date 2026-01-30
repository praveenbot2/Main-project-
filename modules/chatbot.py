"""
Chatbot Module
Interactive health assistant chatbot
"""

import re
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import HEALTH_PARAMS


class HealthChatbot:
    """Interactive chatbot for health queries and guidance"""
    
    def __init__(self):
        self.conversation_history = []
        self.context = {}
    
    def process_message(self, user_message):
        """
        Process user message and generate response
        
        Args:
            user_message: str, user's input message
        
        Returns:
            str, chatbot response
        """
        user_message = user_message.lower().strip()
        self.conversation_history.append(('user', user_message))
        
        # Intent recognition and response generation
        response = self._generate_response(user_message)
        
        self.conversation_history.append(('bot', response))
        return response
    
    def _generate_response(self, message):
        """Generate appropriate response based on message intent"""
        
        # Greeting
        if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
            return ("Hello! I'm your AI Health Assistant. I can help you with:\n"
                   "• Understanding your health metrics\n"
                   "• Explaining vital signs\n"
                   "• Providing health tips\n"
                   "• Answering health-related questions\n"
                   "How can I assist you today?")
        
        # Heart rate queries
        if any(word in message for word in ['heart rate', 'pulse', 'heartbeat']):
            hr_info = HEALTH_PARAMS['heart_rate']
            return (f"Heart Rate Information:\n"
                   f"• Normal range: {hr_info['normal'][0]}-{hr_info['normal'][1]} bpm\n"
                   f"• A normal resting heart rate for adults is 60-100 beats per minute\n"
                   f"• Lower rates may indicate good cardiovascular fitness\n"
                   f"• Higher rates could indicate stress, fever, or other conditions\n"
                   f"• Monitor your heart rate during rest and activity")
        
        # Blood pressure queries
        if any(word in message for word in ['blood pressure', 'bp', 'hypertension']):
            bp_sys = HEALTH_PARAMS['blood_pressure_systolic']
            bp_dia = HEALTH_PARAMS['blood_pressure_diastolic']
            return (f"Blood Pressure Information:\n"
                   f"• Normal systolic: {bp_sys['normal'][0]}-{bp_sys['normal'][1]} mmHg\n"
                   f"• Normal diastolic: {bp_dia['normal'][0]}-{bp_dia['normal'][1]} mmHg\n"
                   f"• High blood pressure (hypertension) can lead to serious health issues\n"
                   f"• Maintain healthy BP through diet, exercise, and stress management\n"
                   f"• Check regularly and consult a doctor if consistently high")
        
        # Temperature queries
        if any(word in message for word in ['temperature', 'fever', 'temp']):
            temp_info = HEALTH_PARAMS['temperature']
            return (f"Body Temperature Information:\n"
                   f"• Normal range: {temp_info['normal'][0]}-{temp_info['normal'][1]}°C (96.8-99.0°F)\n"
                   f"• Fever is generally considered 38°C (100.4°F) or higher\n"
                   f"• Low temperature (hypothermia) is below 35°C (95°F)\n"
                   f"• Body temperature varies throughout the day\n"
                   f"• Seek medical attention for persistent high fever")
        
        # Oxygen saturation queries
        if any(word in message for word in ['oxygen', 'spo2', 'saturation', 'o2']):
            o2_info = HEALTH_PARAMS['oxygen_saturation']
            return (f"Oxygen Saturation Information:\n"
                   f"• Normal range: {o2_info['normal'][0]}-{o2_info['normal'][1]}%\n"
                   f"• SpO2 below 95% may indicate respiratory issues\n"
                   f"• Below 90% is considered low and requires medical attention\n"
                   f"• Measured using a pulse oximeter\n"
                   f"• Important for monitoring respiratory health")
        
        # Respiratory rate queries
        if any(word in message for word in ['breathing', 'respiratory', 'breath']):
            resp_info = HEALTH_PARAMS['respiratory_rate']
            return (f"Respiratory Rate Information:\n"
                   f"• Normal range: {resp_info['normal'][0]}-{resp_info['normal'][1]} breaths/min\n"
                   f"• Rapid breathing may indicate distress or infection\n"
                   f"• Slow breathing might indicate certain medical conditions\n"
                   f"• Practice deep breathing for stress relief\n"
                   f"• Monitor for any persistent changes")
        
        # Risk assessment queries
        if any(word in message for word in ['risk', 'danger', 'safe', 'healthy']):
            return ("Health Risk Assessment:\n"
                   "Our AI system evaluates your vital signs to determine health risk:\n"
                   "• Low Risk: All vitals within normal ranges\n"
                   "• Medium Risk: Some vitals outside normal, needs monitoring\n"
                   "• High Risk: Critical values, requires immediate attention\n\n"
                   "The system continuously monitors and alerts you of any concerns.")
        
        # Emergency queries
        if any(word in message for word in ['emergency', 'urgent', 'critical', '911']):
            return ("🚨 EMERGENCY RESPONSE:\n"
                   "If you're experiencing a medical emergency:\n"
                   "• Call emergency services immediately (911 or local emergency number)\n"
                   "• Don't wait for symptoms to worsen\n"
                   "• Stay calm and follow dispatcher instructions\n\n"
                   "Emergency signs include:\n"
                   "• Chest pain or pressure\n"
                   "• Difficulty breathing\n"
                   "• Severe bleeding\n"
                   "• Loss of consciousness\n"
                   "• Stroke symptoms (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call)")
        
        # Health tips queries
        if any(word in message for word in ['tips', 'advice', 'improve', 'maintain']):
            return ("Health Maintenance Tips:\n"
                   "1. 💓 Cardiovascular: Exercise 30 mins daily, reduce salt intake\n"
                   "2. 🥗 Nutrition: Eat balanced meals, plenty of fruits/vegetables\n"
                   "3. 💧 Hydration: Drink 8 glasses of water daily\n"
                   "4. 😴 Sleep: Get 7-9 hours of quality sleep\n"
                   "5. 🧘 Stress: Practice relaxation techniques, meditation\n"
                   "6. 🚭 Avoid: Smoking, excessive alcohol, drugs\n"
                   "7. 📊 Monitor: Check vitals regularly, attend health checkups")
        
        # Help queries
        if any(word in message for word in ['help', 'what can you do', 'commands']):
            return ("I can help you with:\n"
                   "📊 Vital Signs: Ask about heart rate, blood pressure, temperature, etc.\n"
                   "⚠️ Risk Assessment: Understanding health risk levels\n"
                   "💡 Health Tips: General health and wellness advice\n"
                   "🚨 Emergency Info: What to do in emergencies\n"
                   "❓ Questions: Any health-related queries\n\n"
                   "Just type your question naturally!")
        
        # Thank you
        if any(word in message for word in ['thank', 'thanks', 'appreciate']):
            return ("You're welcome! I'm here to help with your health monitoring. "
                   "Stay healthy and don't hesitate to ask if you have more questions! 😊")
        
        # Goodbye
        if any(word in message for word in ['bye', 'goodbye', 'exit', 'quit']):
            return ("Goodbye! Take care of your health. Remember to monitor your vitals regularly. "
                   "Feel free to return anytime you need assistance! 👋")
        
        # Default response
        return ("I'm here to help with health-related questions. You can ask me about:\n"
               "• Vital signs (heart rate, blood pressure, temperature, etc.)\n"
               "• Health risk assessment\n"
               "• Health tips and advice\n"
               "• Emergency procedures\n\n"
               "What would you like to know?")
    
    def get_conversation_history(self):
        """Return conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.context = {}


if __name__ == "__main__":
    # Test the chatbot
    chatbot = HealthChatbot()
    
    print("Health Chatbot Test")
    print("=" * 60)
    
    test_messages = [
        "Hello",
        "What is a normal heart rate?",
        "Tell me about blood pressure",
        "What should I do in an emergency?",
        "Give me some health tips",
        "Thank you"
    ]
    
    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = chatbot.process_message(msg)
        print(f"Bot: {response}")
        print("-" * 60)
