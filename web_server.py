"""
Web Server Module
Flask-based web interface for AI Health Monitor
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.ai_predictor import HealthPredictor
from modules.alert_system import AlertSystem
from modules.chatbot import HealthChatbot
from modules.real_time_monitor import RealTimeMonitor
from config import HOST, PORT, DEBUG

app = Flask(__name__)
CORS(app)

# Initialize components
predictor = HealthPredictor()
alert_system = AlertSystem()
chatbot = HealthChatbot()
monitor = RealTimeMonitor()

# Load model
try:
    predictor.load_model()
    print("Model loaded successfully")
except:
    print("Warning: Model not loaded. Please train the model first.")


@app.route('/')
def index():
    """Home page"""
    return jsonify({
        'message': 'AI Health Monitor API',
        'status': 'active',
        'endpoints': {
            '/predict': 'POST - Predict health risk',
            '/chat': 'POST - Chat with health assistant',
            '/monitor': 'GET - Get simulated vitals',
            '/alerts': 'GET - Get alert summary',
            '/health': 'GET - Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor.model is not None
    })


@app.route('/predict', methods=['POST'])
def predict():
    """Predict health risk from vital signs"""
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = [
            'heart_rate', 'blood_pressure_systolic', 
            'blood_pressure_diastolic', 'temperature', 
            'oxygen_saturation', 'respiratory_rate'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Make prediction
        prediction = predictor.predict(data)
        
        # Generate alert
        alert = alert_system.check_and_alert(prediction, data)
        
        return jsonify({
            'success': True,
            'vitals': data,
            'prediction': prediction,
            'alert': alert
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    """Chat with health assistant"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        response = chatbot.process_message(message)
        
        return jsonify({
            'success': True,
            'user_message': message,
            'bot_response': response,
            'conversation_history': chatbot.get_conversation_history()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/monitor', methods=['GET'])
def get_monitored_vitals():
    """Get simulated vital signs"""
    try:
        condition = request.args.get('condition', 'healthy')
        vitals = monitor.simulate_vitals(condition)
        
        # Make prediction
        prediction = predictor.predict(vitals)
        
        return jsonify({
            'success': True,
            'timestamp': monitor.monitoring_history[-1]['timestamp'] if monitor.monitoring_history else None,
            'vitals': vitals,
            'prediction': prediction
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/alerts', methods=['GET'])
def get_alerts():
    """Get alert summary"""
    try:
        summary = alert_system.get_alert_summary()
        
        return jsonify({
            'success': True,
            'alerts': summary
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/simulate', methods=['POST'])
def simulate_monitoring():
    """Simulate a monitoring check"""
    try:
        data = request.get_json()
        condition = data.get('condition', 'healthy')
        
        # Simulate vitals
        vitals = monitor.simulate_vitals(condition)
        
        # Perform monitoring check
        result = monitor.monitor_once(vitals)
        
        return jsonify({
            'success': True,
            'monitoring_result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("AI Health Monitor Web Server")
    print("="*70)
    print(f"Starting server on http://{HOST}:{PORT}")
    print("API Endpoints:")
    print("  POST /predict - Health risk prediction")
    print("  POST /chat - Chatbot interaction")
    print("  GET  /monitor - Get monitored vitals")
    print("  GET  /alerts - Alert summary")
    print("  POST /simulate - Simulate monitoring")
    print("="*70 + "\n")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
