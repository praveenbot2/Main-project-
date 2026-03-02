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

# Initialize components (shared instances so alerts are unified)
predictor = HealthPredictor()
alert_system = AlertSystem()
chatbot = HealthChatbot()
monitor = RealTimeMonitor(predictor=predictor, alert_system=alert_system)

# Load model
try:
    predictor.load_model()
    print("Model loaded successfully")
except Exception as e:
    print(f"Warning: Model not loaded - {e}. Please train the model first.")


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
        data = request.get_json(force=False, silent=False)
    except Exception as e:
        return jsonify({'error': 'Invalid JSON in request body'}), 400
    
    try:
        if data is None:
            return jsonify({'error': 'Invalid JSON in request body'}), 400
        
        # Validate input
        required_fields = [
            'heart_rate', 'blood_pressure_systolic', 
            'blood_pressure_diastolic', 'temperature', 
            'oxygen_saturation', 'respiratory_rate'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Validate ranges
        from config import HEALTH_PARAMS
        validations = {
            'heart_rate': HEALTH_PARAMS['heart_rate'],
            'blood_pressure_systolic': HEALTH_PARAMS['blood_pressure_systolic'],
            'blood_pressure_diastolic': HEALTH_PARAMS['blood_pressure_diastolic'],
            'temperature': HEALTH_PARAMS['temperature'],
            'oxygen_saturation': HEALTH_PARAMS['oxygen_saturation'],
            'respiratory_rate': HEALTH_PARAMS['respiratory_rate']
        }
        
        for field, limits in validations.items():
            value = data[field]
            if not isinstance(value, (int, float)):
                return jsonify({'error': f'{field} must be a number'}), 400
            if value < limits['min'] or value > limits['max']:
                return jsonify({'error': f'{field} must be between {limits["min"]} and {limits["max"]}'}), 400
        
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
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/chat', methods=['POST'])
def chat():
    """Chat with health assistant"""
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Invalid JSON in request body'}), 400
        
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
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/monitor', methods=['GET'])
def get_monitored_vitals():
    """Get simulated vital signs"""
    try:
        condition = request.args.get('condition', 'healthy')
        
        if condition not in ['healthy', 'at_risk', 'critical']:
            return jsonify({'error': 'condition must be one of: healthy, at_risk, critical'}), 400
        
        vitals = monitor.simulate_vitals(condition)
        
        # Make prediction
        prediction = predictor.predict(vitals)
        
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'timestamp': timestamp,
            'vitals': vitals,
            'prediction': prediction
        })
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


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
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/simulate', methods=['POST'])
def simulate_monitoring():
    """Simulate a monitoring check"""
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Invalid JSON in request body'}), 400
        
        condition = data.get('condition', 'healthy')
        
        if condition not in ['healthy', 'at_risk', 'critical']:
            return jsonify({'error': 'condition must be one of: healthy, at_risk, critical'}), 400
        
        # Simulate vitals
        vitals = monitor.simulate_vitals(condition)
        
        # Perform monitoring check
        result = monitor.monitor_once(vitals)
        
        return jsonify({
            'success': True,
            'monitoring_result': result
        })
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


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
