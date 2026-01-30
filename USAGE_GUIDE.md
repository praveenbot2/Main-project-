# Usage Guide - AI Health Monitor System

This guide provides detailed instructions for using the AI-Driven Health Monitoring and Alert System.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Module-by-Module Usage](#module-by-module-usage)
3. [Web API Usage](#web-api-usage)
4. [Advanced Usage](#advanced-usage)
5. [Examples](#examples)

## Quick Start

### First-Time Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Initial Setup**
   ```bash
   python main.py
   ```
   This will:
   - Generate synthetic health dataset
   - Train the AI model
   - Save the model for future use

3. **Run Demo**
   ```bash
   python demo.py
   ```

## Module-by-Module Usage

### 1. Data Generator

Generate synthetic health monitoring dataset:

```python
from modules.data_generator import DataGenerator

# Create generator with 1000 samples
generator = DataGenerator(size=1000)

# Generate and save dataset
df = generator.save_dataset('data/health_data.csv')

# Or just generate without saving
df = generator.generate_health_data()
print(df.head())
```

### 2. AI Predictor

Predict health risk from vital signs:

```python
from modules.ai_predictor import HealthPredictor

# Initialize predictor
predictor = HealthPredictor()

# Load pre-trained model
predictor.load_model()

# Or train new model
# predictor.train('data/health_data.csv')

# Make prediction
vitals = {
    'heart_rate': 75.0,
    'blood_pressure_systolic': 120.0,
    'blood_pressure_diastolic': 80.0,
    'temperature': 36.8,
    'oxygen_saturation': 98.0,
    'respiratory_rate': 16.0
}

result = predictor.predict(vitals)
print(f"Risk Level: {result['risk_level']}")
print(f"Confidence: {result['probability']}")
print(f"Recommendations: {result['recommendations']}")
```

### 3. Alert System

Monitor and generate alerts:

```python
from modules.alert_system import AlertSystem

# Initialize alert system
alert_system = AlertSystem()

# Check and generate alert
alert = alert_system.check_and_alert(prediction_result, vitals)

print(f"Alert Type: {alert['alert_type']}")
print(f"Message: {alert['message']}")

# Get alert summary
summary = alert_system.get_alert_summary()
print(f"Total Alerts: {summary['total_alerts']}")
print(f"Critical: {summary['critical']}")
```

### 4. Chatbot

Interactive health assistant:

```python
from modules.chatbot import HealthChatbot

# Initialize chatbot
chatbot = HealthChatbot()

# Process user messages
response = chatbot.process_message("What is a normal heart rate?")
print(response)

# Get conversation history
history = chatbot.get_conversation_history()
```

### 5. Real-Time Monitor

Continuous health monitoring:

```python
from modules.real_time_monitor import RealTimeMonitor

# Initialize monitor
monitor = RealTimeMonitor()

# Run continuous monitoring
# Duration in seconds, interval between checks, condition simulation
monitor.continuous_monitor(
    duration_seconds=60,
    interval_seconds=5,
    condition='healthy'  # Options: 'healthy', 'at_risk', 'critical'
)

# Single check
vitals = monitor.simulate_vitals('healthy')
result = monitor.monitor_once(vitals)
```

## Web API Usage

### Starting the Server

```bash
python web_server.py
```

Server runs on `http://localhost:5000`

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:5000/health
```

#### 2. Predict Health Risk
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 75,
    "blood_pressure_systolic": 120,
    "blood_pressure_diastolic": 80,
    "temperature": 36.8,
    "oxygen_saturation": 98,
    "respiratory_rate": 16
  }'
```

#### 3. Chat with Assistant
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a normal heart rate?"}'
```

#### 4. Get Monitored Vitals
```bash
# Healthy condition
curl http://localhost:5000/monitor?condition=healthy

# At-risk condition
curl http://localhost:5000/monitor?condition=at_risk

# Critical condition
curl http://localhost:5000/monitor?condition=critical
```

#### 5. Get Alert Summary
```bash
curl http://localhost:5000/alerts
```

#### 6. Simulate Monitoring Check
```bash
curl -X POST http://localhost:5000/simulate \
  -H "Content-Type: application/json" \
  -d '{"condition": "healthy"}'
```

## Advanced Usage

### Custom Model Training

Train model with custom parameters:

```python
from modules.ai_predictor import HealthPredictor
from sklearn.ensemble import RandomForestClassifier

predictor = HealthPredictor()

# Customize model before training
predictor.model = RandomForestClassifier(
    n_estimators=200,  # More trees
    max_depth=15,      # Deeper trees
    random_state=42
)

predictor.train('data/health_data.csv')
```

### Custom Alert Thresholds

Modify `config.py`:

```python
ALERT_THRESHOLDS = {
    'high_risk': 0.8,    # More conservative
    'medium_risk': 0.5,
    'low_risk': 0.2
}
```

### Custom Health Parameters

Modify `config.py` to adjust normal ranges:

```python
HEALTH_PARAMS = {
    'heart_rate': {'min': 40, 'max': 200, 'normal': (55, 95)},
    # ... other parameters
}
```

## Examples

### Example 1: Complete Health Check Pipeline

```python
from modules.ai_predictor import HealthPredictor
from modules.alert_system import AlertSystem

# Initialize
predictor = HealthPredictor()
predictor.load_model()
alert_system = AlertSystem()

# Patient vitals
patient_vitals = {
    'heart_rate': 110.0,
    'blood_pressure_systolic': 145.0,
    'blood_pressure_diastolic': 92.0,
    'temperature': 37.5,
    'oxygen_saturation': 93.0,
    'respiratory_rate': 22.0
}

# Predict
prediction = predictor.predict(patient_vitals)

# Generate alert
alert = alert_system.check_and_alert(prediction, patient_vitals)

# Display results
print(f"Risk: {prediction['risk_level']} ({prediction['probability']})")
print(f"Alert: {alert['message']}")
for rec in prediction['recommendations']:
    print(f"  - {rec}")
```

### Example 2: Batch Processing

```python
import pandas as pd
from modules.ai_predictor import HealthPredictor

# Load data
df = pd.read_csv('patient_data.csv')

# Initialize predictor
predictor = HealthPredictor()
predictor.load_model()

# Process each patient
results = []
for _, row in df.iterrows():
    vitals = row.to_dict()
    prediction = predictor.predict(vitals)
    results.append({
        'patient_id': row['id'],
        'risk_level': prediction['risk_level'],
        'probability': prediction['probability']
    })

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('risk_assessment_results.csv', index=False)
```

### Example 3: Interactive Monitoring Session

```python
from modules.real_time_monitor import RealTimeMonitor

monitor = RealTimeMonitor()

# Initialize
if monitor.initialize():
    # Monitor for 5 minutes, check every 10 seconds
    monitor.continuous_monitor(
        duration_seconds=300,
        interval_seconds=10,
        condition='healthy'
    )
    
    # Get monitoring history
    history = monitor.get_history(last_n=10)
    print(f"Last 10 checks: {len(history)}")

```

### Example 4: Chatbot Integration

```python
from modules.chatbot import HealthChatbot

chatbot = HealthChatbot()

# Conversation loop
print("Health Assistant (type 'exit' to quit)")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'exit':
        break
    
    response = chatbot.process_message(user_input)
    print(f"Assistant: {response}")
```

## Troubleshooting

### Model Not Found Error
If you see "Model not found", run:
```bash
python modules/ai_predictor.py
```

### Import Errors
Make sure you're running from the project root directory and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port Already in Use
If the web server port is in use, change it in `config.py`:
```python
PORT = 5001  # Use different port
```

## Best Practices

1. **Regular Model Retraining**: Retrain the model periodically with new data
2. **Alert Threshold Tuning**: Adjust thresholds based on your use case
3. **Data Validation**: Always validate input vitals before prediction
4. **Error Handling**: Implement proper error handling in production
5. **Logging**: Add logging for monitoring and debugging

## Support

For issues or questions:
- Check the README.md for general information
- Review this usage guide
- Open an issue on GitHub
