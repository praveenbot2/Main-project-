"""
Smart Chatbot Module
NLP-powered health assistant with TF-IDF intent matching,
medical knowledge base, and symptom checker
"""

import re
import sys
import os
import numpy as np
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HEALTH_PARAMS

# ---------------------------------------------------------------------------
# Medical Knowledge Base
# ---------------------------------------------------------------------------

KNOWLEDGE_BASE = {
    'heart_rate': {
        'title': 'Heart Rate',
        'normal': '60–100 bpm',
        'info': (
            'A normal resting heart rate for adults is 60–100 beats per minute. '
            'Lower rates may indicate good cardiovascular fitness. '
            'Higher rates could indicate stress, fever, dehydration, or cardiac conditions. '
            'Persistent tachycardia (>100 bpm) or bradycardia (<60 bpm) should be evaluated.'
        ),
        'tips': [
            'Regular aerobic exercise strengthens the heart',
            'Reduce caffeine and alcohol intake',
            'Practice deep breathing or meditation for stress reduction',
            'Stay hydrated throughout the day',
        ],
    },
    'blood_pressure': {
        'title': 'Blood Pressure',
        'normal': 'Systolic 90–120 mmHg, Diastolic 60–80 mmHg',
        'info': (
            'Blood pressure is the force of blood against artery walls. '
            'Hypertension (>130/80) increases risk of heart disease and stroke. '
            'Hypotension (<90/60) can cause dizziness and fainting. '
            'Regular monitoring is important for early detection.'
        ),
        'tips': [
            'Reduce sodium intake to <2,300 mg/day',
            'Maintain a healthy weight (BMI 18.5–24.9)',
            'Exercise 150 minutes per week',
            'Limit alcohol consumption',
            'Manage stress through relaxation techniques',
        ],
    },
    'temperature': {
        'title': 'Body Temperature',
        'normal': '36.1–37.2°C (96.8–99.0°F)',
        'info': (
            'Normal body temperature averages ~37°C (98.6°F) but varies throughout the day. '
            'Fever ≥38°C (100.4°F) is the body\'s response to infection. '
            'Hypothermia <35°C (95°F) is a medical emergency. '
            'Temperature can be affected by exercise, hormones, and environment.'
        ),
        'tips': [
            'Stay hydrated with fluids during fever',
            'Dress appropriately for weather conditions',
            'Seek medical attention for fever >39.4°C (103°F)',
            'Use a reliable thermometer for accurate readings',
        ],
    },
    'oxygen_saturation': {
        'title': 'Oxygen Saturation (SpO2)',
        'normal': '95–100%',
        'info': (
            'SpO2 measures the percentage of hemoglobin bound to oxygen. '
            'Values below 95% may indicate respiratory issues. '
            'Below 90% is considered hypoxemia and requires medical attention. '
            'Chronic conditions like COPD may have different baseline values.'
        ),
        'tips': [
            'Practice deep breathing exercises',
            'Avoid smoking and secondhand smoke',
            'Maintain good posture for optimal lung capacity',
            'Use a pulse oximeter for regular monitoring',
        ],
    },
    'respiratory_rate': {
        'title': 'Respiratory Rate',
        'normal': '12–20 breaths per minute',
        'info': (
            'Normal adult respiratory rate is 12–20 breaths per minute at rest. '
            'Tachypnea (>20) may indicate infection, anxiety, or respiratory distress. '
            'Bradypnea (<12) might suggest CNS depression or certain medications. '
            'Rate should be measured at rest for accuracy.'
        ),
        'tips': [
            'Practice diaphragmatic breathing',
            'Regular cardiovascular exercise improves lung capacity',
            'Avoid environmental pollutants',
            'Maintain good posture for efficient breathing',
        ],
    },
}

# ---------------------------------------------------------------------------
# Symptom Checker Knowledge
# ---------------------------------------------------------------------------

SYMPTOM_TRIAGE = {
    'chest_pain': {
        'question': 'Are you experiencing chest pain or chest tightness?',
        'severity': 'high',
        'followups': [
            'Is the pain sharp or crushing?',
            'Does it radiate to your arm, jaw, or back?',
            'Are you also short of breath?',
        ],
        'advice': (
            '🚨 Chest pain can indicate a cardiac emergency. '
            'If the pain is severe, crushing, or radiates to your arm/jaw, '
            'call emergency services (911) immediately. '
            'Do not drive yourself to the hospital.'
        ),
    },
    'shortness_of_breath': {
        'question': 'Are you having difficulty breathing or shortness of breath?',
        'severity': 'high',
        'followups': [
            'Did it come on suddenly?',
            'Is it worse when lying down?',
            'Do you have a cough or wheezing?',
        ],
        'advice': (
            '⚠️ Sudden shortness of breath can be serious. '
            'If severe or with chest pain, seek emergency care. '
            'If mild and chronic, schedule a doctor visit for evaluation. '
            'Check your SpO2 — below 92% warrants urgent attention.'
        ),
    },
    'dizziness': {
        'question': 'Are you feeling dizzy or lightheaded?',
        'severity': 'medium',
        'followups': [
            'Did it start suddenly?',
            'Have you been drinking enough water?',
            'Have you eaten recently?',
        ],
        'advice': (
            'Dizziness can be caused by dehydration, low blood sugar, '
            'low blood pressure, or inner ear issues. '
            'Sit or lie down until it passes. Hydrate and eat a small snack. '
            'If it persists or is accompanied by vision changes, seek medical care.'
        ),
    },
    'headache': {
        'question': 'Are you experiencing a headache?',
        'severity': 'low',
        'followups': [
            'Is it the worst headache of your life?',
            'Do you have fever or neck stiffness?',
            'Have you had any vision changes?',
        ],
        'advice': (
            'Most headaches are tension-type and resolve with rest and hydration. '
            'A sudden, severe "thunderclap" headache or one with fever and '
            'neck stiffness requires immediate emergency evaluation. '
            'Over-the-counter pain relief may help mild headaches.'
        ),
    },
    'fatigue': {
        'question': 'Are you experiencing unusual fatigue or weakness?',
        'severity': 'low',
        'followups': [
            'How long have you felt this way?',
            'Are you sleeping well?',
            'Have you noticed any other symptoms?',
        ],
        'advice': (
            'Fatigue can result from poor sleep, stress, dehydration, or underlying '
            'conditions like anemia or thyroid issues. '
            'Ensure 7–9 hours of sleep, stay hydrated, and eat balanced meals. '
            'If fatigue persists >2 weeks, consult your doctor for blood work.'
        ),
    },
    'fever': {
        'question': 'Do you have a fever or feel feverish?',
        'severity': 'medium',
        'followups': [
            'What is your temperature?',
            'How long have you had it?',
            'Do you have any other symptoms (cough, body aches)?',
        ],
        'advice': (
            'Fever is your body fighting infection. Stay hydrated and rest. '
            'Seek medical attention if: temperature >39.4°C (103°F), '
            'fever lasts >3 days, or you have severe symptoms like '
            'difficulty breathing, confusion, or persistent vomiting.'
        ),
    },
}

# ---------------------------------------------------------------------------
# Intent Training Data (for TF-IDF matching)
# ---------------------------------------------------------------------------

INTENT_EXAMPLES = {
    'greeting': [
        'hello', 'hi', 'hey', 'good morning', 'good afternoon',
        'greetings', 'howdy', 'whats up', 'hi there',
    ],
    'heart_rate': [
        'heart rate', 'pulse', 'heartbeat', 'bpm', 'heart beats',
        'tachycardia', 'bradycardia', 'resting heart rate',
        'what is my heart rate', 'tell me about pulse',
    ],
    'blood_pressure': [
        'blood pressure', 'bp', 'hypertension', 'systolic', 'diastolic',
        'high blood pressure', 'low blood pressure', 'hypotension',
    ],
    'temperature': [
        'temperature', 'fever', 'body temp', 'hypothermia',
        'high temperature', 'am i feverish', 'body heat',
    ],
    'oxygen': [
        'oxygen', 'spo2', 'saturation', 'o2 level', 'oxygen level',
        'pulse oximeter', 'hypoxia', 'oxygen saturation',
    ],
    'respiratory': [
        'breathing', 'respiratory rate', 'breath', 'breaths per minute',
        'tachypnea', 'breathing rate', 'lung function',
    ],
    'risk': [
        'risk', 'danger', 'safe', 'healthy', 'risk level',
        'health status', 'am i healthy', 'risk assessment',
    ],
    'emergency': [
        'emergency', 'urgent', 'critical', '911', 'call ambulance',
        'heart attack', 'stroke', 'cant breathe', 'help me',
    ],
    'tips': [
        'tips', 'advice', 'improve', 'maintain', 'wellness',
        'how to be healthy', 'health advice', 'suggestions',
    ],
    'symptom_check': [
        'symptom', 'symptoms', 'check symptoms', 'whats wrong',
        'i feel sick', 'diagnose', 'symptom checker',
        'i have pain', 'something is wrong', 'feeling unwell',
    ],
    'chest_pain': [
        'chest pain', 'chest hurts', 'chest tightness', 'pain in chest',
        'pressure in chest', 'heart pain',
    ],
    'shortness_of_breath': [
        'shortness of breath', 'cant breathe', 'hard to breathe',
        'breathing difficulty', 'breathless', 'dyspnea',
    ],
    'dizziness': [
        'dizzy', 'dizziness', 'lightheaded', 'feel faint',
        'room spinning', 'vertigo',
    ],
    'headache': [
        'headache', 'head hurts', 'migraine', 'head pain',
        'throbbing head', 'pounding head',
    ],
    'fatigue': [
        'tired', 'fatigue', 'exhausted', 'no energy',
        'weak', 'lethargic', 'drowsy', 'sleepy all the time',
    ],
    'fever_symptom': [
        'fever', 'feverish', 'high temperature', 'chills',
        'sweating', 'feel hot',
    ],
    'help': [
        'help', 'what can you do', 'commands', 'menu',
        'options', 'capabilities', 'how to use',
    ],
    'thanks': [
        'thank', 'thanks', 'appreciate', 'thank you', 'thx',
    ],
    'goodbye': [
        'bye', 'goodbye', 'exit', 'quit', 'see you', 'later',
    ],
}


class SmartChatbot:
    """NLP-powered health chatbot with TF-IDF intent matching."""

    def __init__(self):
        self.conversation_history = []
        self.context = {}
        self.latest_vitals = None
        # Build TF-IDF vocabulary
        self._vocab = {}
        self._idf = {}
        self._intent_vectors = {}
        self._build_tfidf()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_message(self, user_message, vitals=None):
        """Process a user message and return a response."""
        if vitals:
            self.latest_vitals = vitals

        msg_clean = user_message.lower().strip()
        self.conversation_history.append(('user', user_message))

        intent, confidence = self._classify_intent(msg_clean)
        response = self._generate_response(intent, msg_clean, confidence)

        self.conversation_history.append(('bot', response))
        return response

    def set_vitals(self, vitals):
        """Inject the latest vitals for context-aware responses."""
        self.latest_vitals = vitals

    def get_conversation_history(self):
        return [{'role': role, 'message': msg} for role, msg in self.conversation_history]

    def clear_history(self):
        self.conversation_history = []
        self.context = {}

    # ------------------------------------------------------------------
    # TF-IDF intent classifier
    # ------------------------------------------------------------------

    def _build_tfidf(self):
        """Build a simple TF-IDF model from intent examples."""
        # Collect all documents
        all_docs = []
        doc_labels = []
        for intent, examples in INTENT_EXAMPLES.items():
            for ex in examples:
                tokens = self._tokenize(ex)
                all_docs.append(tokens)
                doc_labels.append(intent)

        # Build vocabulary
        vocab = {}
        idx = 0
        for doc in all_docs:
            for token in doc:
                if token not in vocab:
                    vocab[token] = idx
                    idx += 1
        self._vocab = vocab

        # Compute IDF
        n_docs = len(all_docs)
        doc_freq = defaultdict(int)
        for doc in all_docs:
            seen = set(doc)
            for token in seen:
                doc_freq[token] += 1

        self._idf = {}
        for token, df in doc_freq.items():
            self._idf[token] = np.log((n_docs + 1) / (df + 1)) + 1  # smoothed IDF

        # Compute intent centroid vectors
        intent_vecs = defaultdict(list)
        for doc, label in zip(all_docs, doc_labels):
            vec = self._tfidf_vector(doc)
            intent_vecs[label].append(vec)

        self._intent_vectors = {}
        for intent, vecs in intent_vecs.items():
            centroid = np.mean(vecs, axis=0)
            norm = np.linalg.norm(centroid)
            if norm > 0:
                centroid /= norm
            self._intent_vectors[intent] = centroid

    def _tfidf_vector(self, tokens):
        """Convert token list to a TF-IDF vector."""
        vec = np.zeros(len(self._vocab))
        tf = defaultdict(int)
        for t in tokens:
            tf[t] += 1
        for t, freq in tf.items():
            if t in self._vocab:
                vec[self._vocab[t]] = freq * self._idf.get(t, 1.0)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec

    def _classify_intent(self, message):
        """Return (intent, confidence) using cosine similarity."""
        tokens = self._tokenize(message)
        if not tokens:
            return 'unknown', 0.0

        vec = self._tfidf_vector(tokens)
        best_intent = 'unknown'
        best_score = 0.0

        for intent, centroid in self._intent_vectors.items():
            score = float(np.dot(vec, centroid))
            if score > best_score:
                best_score = score
                best_intent = intent

        return best_intent, best_score

    @staticmethod
    def _tokenize(text):
        """Simple whitespace + punctuation tokenizer."""
        text = re.sub(r'[^a-z0-9\s]', ' ', text.lower())
        return [t for t in text.split() if len(t) > 1]

    # ------------------------------------------------------------------
    # Response generation
    # ------------------------------------------------------------------

    def _generate_response(self, intent, message, confidence):
        """Generate a response based on classified intent."""

        # Low confidence → fallback
        if confidence < 0.15:
            return self._default_response()

        # --- Greetings ---
        if intent == 'greeting':
            vitals_note = ''
            if self.latest_vitals:
                vitals_note = '\n\nI can see your latest vitals — ask me to analyze them!'
            return (
                "Hello! I'm your AI Health Assistant. I can help you with:\n"
                "• Understanding vital signs and health metrics\n"
                "• Symptom assessment and triage suggestions\n"
                "• Personalized health tips\n"
                "• Analyzing your latest readings" + vitals_note
            )

        # --- Vital sign info (knowledge base) ---
        kb_map = {
            'heart_rate': 'heart_rate',
            'blood_pressure': 'blood_pressure',
            'temperature': 'temperature',
            'oxygen': 'oxygen_saturation',
            'respiratory': 'respiratory_rate',
        }
        if intent in kb_map:
            return self._kb_response(kb_map[intent])

        # --- Risk assessment ---
        if intent == 'risk':
            return self._risk_response()

        # --- Emergency ---
        if intent == 'emergency':
            return (
                "🚨 EMERGENCY RESPONSE:\n"
                "If you're experiencing a medical emergency:\n"
                "• Call emergency services immediately (911 or local number)\n"
                "• Don't wait for symptoms to worsen\n"
                "• Stay calm and follow dispatcher instructions\n\n"
                "Emergency signs: chest pain, difficulty breathing, "
                "severe bleeding, loss of consciousness, stroke symptoms "
                "(FAST: Face drooping, Arm weakness, Speech difficulty, Time to call)"
            )

        # --- Tips ---
        if intent == 'tips':
            return self._tips_response()

        # --- Symptom checker ---
        if intent == 'symptom_check':
            return self._symptom_menu()

        # --- Specific symptoms ---
        symptom_map = {
            'chest_pain': 'chest_pain',
            'shortness_of_breath': 'shortness_of_breath',
            'dizziness': 'dizziness',
            'headache': 'headache',
            'fatigue': 'fatigue',
            'fever_symptom': 'fever',
        }
        if intent in symptom_map:
            return self._symptom_response(symptom_map[intent])

        # --- Help ---
        if intent == 'help':
            return (
                "I can help you with:\n"
                "📊 **Vital Signs** — Ask about heart rate, blood pressure, temperature, etc.\n"
                "🩺 **Symptom Checker** — Describe symptoms for triage guidance\n"
                "⚠️ **Risk Assessment** — Understand health risk levels\n"
                "💡 **Health Tips** — Wellness advice tailored to your vitals\n"
                "🚨 **Emergency Info** — What to do in emergencies\n\n"
                "Try: \"check my symptoms\", \"tell me about blood pressure\", "
                "\"analyze my vitals\""
            )

        # --- Thanks / Goodbye ---
        if intent == 'thanks':
            return "You're welcome! Stay healthy and don't hesitate to ask more questions. 😊"
        if intent == 'goodbye':
            return "Goodbye! Remember to monitor your vitals regularly. Take care! 👋"

        return self._default_response()

    # ------------------------------------------------------------------
    # Knowledge-base responses
    # ------------------------------------------------------------------

    def _kb_response(self, topic):
        """Return a knowledge-base response, enriched with current vitals if available."""
        kb = KNOWLEDGE_BASE.get(topic, KNOWLEDGE_BASE.get(topic.replace('_saturation', ''), {}))
        if not kb:
            return self._default_response()

        parts = [
            f"**{kb['title']}**\n",
            f"Normal range: {kb['normal']}\n",
            kb['info'],
        ]

        # Context-aware: include current reading if available
        if self.latest_vitals:
            vital_key = topic
            if topic == 'blood_pressure':
                sys_v = self.latest_vitals.get('blood_pressure_systolic')
                dia_v = self.latest_vitals.get('blood_pressure_diastolic')
                if sys_v is not None:
                    parts.append(f"\n📊 Your current reading: {sys_v}/{dia_v} mmHg")
                    if sys_v > 130 or dia_v > 85:
                        parts.append("⚠️ Your blood pressure appears elevated.")
                    elif sys_v < 90 or dia_v < 60:
                        parts.append("⚠️ Your blood pressure appears low.")
                    else:
                        parts.append("✓ Your blood pressure is within normal range.")
            elif topic == 'oxygen_saturation':
                val = self.latest_vitals.get('oxygen_saturation')
                if val is not None:
                    parts.append(f"\n📊 Your current SpO2: {val}%")
                    if val < 95:
                        parts.append("⚠️ Your oxygen saturation is below normal.")
                    else:
                        parts.append("✓ Your oxygen saturation is normal.")
            else:
                val = self.latest_vitals.get(vital_key)
                if val is not None:
                    limits = HEALTH_PARAMS.get(vital_key, {}).get('normal', (None, None))
                    parts.append(f"\n📊 Your current reading: {val}")
                    if limits[0] is not None and val < limits[0]:
                        parts.append(f"⚠️ Below normal range ({limits[0]}–{limits[1]})")
                    elif limits[1] is not None and val > limits[1]:
                        parts.append(f"⚠️ Above normal range ({limits[0]}–{limits[1]})")
                    else:
                        parts.append(f"✓ Within normal range ({limits[0]}–{limits[1]})")

        # Tips
        tips = kb.get('tips', [])
        if tips:
            parts.append("\n💡 Tips:")
            for tip in tips:
                parts.append(f"  • {tip}")

        return '\n'.join(parts)

    def _risk_response(self):
        resp = (
            "**Health Risk Assessment**\n\n"
            "Our AI evaluates your vitals to determine health risk:\n"
            "• **Low Risk** — All vitals within normal ranges\n"
            "• **Medium Risk** — Some vitals outside normal, needs monitoring\n"
            "• **High Risk** — Critical values, requires immediate attention\n"
        )
        if self.latest_vitals:
            resp += "\n📊 Your latest vitals are loaded. Use the Health Check page for a full prediction."
        return resp

    def _tips_response(self):
        tips = [
            "**Health Maintenance Tips:**",
            "1. 💓 Exercise 30 minutes daily for cardiovascular health",
            "2. 🥗 Eat balanced meals with fruits, vegetables, and whole grains",
            "3. 💧 Drink 8 glasses (2L) of water daily",
            "4. 😴 Get 7–9 hours of quality sleep",
            "5. 🧘 Practice stress management (meditation, deep breathing)",
            "6. 🚭 Avoid smoking and limit alcohol",
            "7. 📊 Monitor vitals regularly and attend checkups",
        ]

        # Personalized tips based on vitals
        if self.latest_vitals:
            tips.append("\n**Based on your current readings:**")
            v = self.latest_vitals
            if v.get('heart_rate', 0) > 90:
                tips.append("• Your heart rate is elevated — consider relaxation techniques")
            if v.get('blood_pressure_systolic', 0) > 125:
                tips.append("• Your blood pressure is on the higher side — reduce salt intake")
            if v.get('oxygen_saturation', 100) < 96:
                tips.append("• Your SpO2 is slightly low — practice deep breathing exercises")
            if v.get('temperature', 37) > 37.3:
                tips.append("• Your temperature is slightly elevated — stay hydrated")

        return '\n'.join(tips)

    # ------------------------------------------------------------------
    # Symptom checker
    # ------------------------------------------------------------------

    def _symptom_menu(self):
        lines = [
            "🩺 **Symptom Checker**\n",
            "Tell me which symptom you're experiencing:\n",
        ]
        for key, info in SYMPTOM_TRIAGE.items():
            severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
            icon = severity_icon.get(info['severity'], '⚪')
            nice_name = key.replace('_', ' ').title()
            lines.append(f"  {icon} {nice_name}")

        lines.append("\nOr simply describe how you're feeling and I'll help assess it.")
        return '\n'.join(lines)

    def _symptom_response(self, symptom_key):
        info = SYMPTOM_TRIAGE.get(symptom_key)
        if not info:
            return "I'm not sure about that symptom. Can you describe it differently?"

        severity_labels = {'high': '🔴 HIGH', 'medium': '🟡 MEDIUM', 'low': '🟢 LOW'}
        lines = [
            f"**{symptom_key.replace('_', ' ').title()}** — Severity: {severity_labels.get(info['severity'], 'UNKNOWN')}\n",
            info['advice'],
            "\n**Questions to consider:**",
        ]
        for q in info['followups']:
            lines.append(f"  • {q}")

        # Add vitals context if available
        if self.latest_vitals:
            lines.append("\n📊 **Your current vitals context:**")
            v = self.latest_vitals
            if symptom_key in ('chest_pain', 'shortness_of_breath'):
                lines.append(f"  Heart rate: {v.get('heart_rate', 'N/A')} bpm")
                lines.append(f"  SpO2: {v.get('oxygen_saturation', 'N/A')}%")
                lines.append(f"  BP: {v.get('blood_pressure_systolic', 'N/A')}/{v.get('blood_pressure_diastolic', 'N/A')} mmHg")
            elif symptom_key == 'fever':
                lines.append(f"  Temperature: {v.get('temperature', 'N/A')}°C")
                lines.append(f"  Heart rate: {v.get('heart_rate', 'N/A')} bpm")

        lines.append('\n⚕️ This is not a medical diagnosis. Consult a healthcare professional for proper evaluation.')
        return '\n'.join(lines)

    def _default_response(self):
        return (
            "I can help with health-related questions. Try asking about:\n"
            "• **Vital signs** — heart rate, blood pressure, temperature, SpO2, respiratory rate\n"
            "• **Symptom checker** — say \"check my symptoms\" or describe how you feel\n"
            "• **Health tips** — personalized wellness advice\n"
            "• **Risk assessment** — understanding your health risk level\n\n"
            "What would you like to know?"
        )


# ---------------------------------------------------------------------------
# Backward-compatible wrapper
# ---------------------------------------------------------------------------

class HealthChatbot:
    """
    Drop-in replacement for the original rule-based chatbot.
    Delegates to SmartChatbot internally.
    """

    def __init__(self):
        self._smart = SmartChatbot()

    def process_message(self, user_message, vitals=None):
        return self._smart.process_message(user_message, vitals)

    def set_vitals(self, vitals):
        self._smart.set_vitals(vitals)

    def get_conversation_history(self):
        return self._smart.get_conversation_history()

    def clear_history(self):
        self._smart.clear_history()


if __name__ == "__main__":
    bot = SmartChatbot()
    print("Smart Health Chatbot Test")
    print("=" * 60)

    test_messages = [
        "Hello",
        "What is a normal heart rate?",
        "Tell me about blood pressure",
        "Check my symptoms",
        "I have chest pain",
        "I feel dizzy",
        "Give me health tips",
        "What's my risk level?",
        "Thank you",
    ]

    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = bot.process_message(msg)
        print(f"Bot: {response}")
        print("-" * 60)
