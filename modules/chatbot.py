"""
Chatbot Module
Interactive health assistant chatbot — now powered by NLP (SmartChatbot)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.smart_chatbot import SmartChatbot


class HealthChatbot:
    """Interactive chatbot for health queries and guidance.
    
    Delegates to SmartChatbot (TF-IDF intent matching, symptom checker,
    medical knowledge base, context-aware responses).
    """

    def __init__(self):
        self._smart = SmartChatbot()

    def process_message(self, user_message, vitals=None):
        return self._smart.process_message(user_message, vitals)

    def set_vitals(self, vitals):
        """Inject the latest vitals for context-aware responses."""
        self._smart.set_vitals(vitals)

    def get_conversation_history(self):
        return self._smart.get_conversation_history()

    def clear_history(self):
        self._smart.clear_history()


if __name__ == "__main__":
    chatbot = HealthChatbot()

    print("Health Chatbot Test")
    print("=" * 60)

    test_messages = [
        "Hello",
        "What is a normal heart rate?",
        "Tell me about blood pressure",
        "What should I do in an emergency?",
        "Give me some health tips",
        "Check my symptoms",
        "I have a headache",
        "Thank you",
    ]

    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = chatbot.process_message(msg)
        print(f"Bot: {response}")
        print("-" * 60)
