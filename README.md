# AI-Driven Health Monitoring and Alert System

A comprehensive real-time health monitoring system powered by AI that tracks vital signs, predicts health risks, generates alerts, and provides interactive health assistance through a chatbot.

## 🌟 Features

- **Dataset-Based AI**: Uses machine learning trained on synthetic health data to predict health risks
- **Real-Time Prediction**: Continuous monitoring and instant health risk assessment
- **Alert System**: Intelligent alert generation based on health risk levels (Critical, Warning, Info)
- **Chatbot Module**: Interactive health assistant to answer health-related questions
- **Modular Architecture**: Clean, modular design for easy maintenance and extension

## 🏗️ Architecture

The system is built with a modular architecture consisting of:

```
AI_Health_Monitor/
├── config.py                   # Configuration settings
├── main.py                     # Main application entry point
├── web_server.py              # Flask web API server
├── requirements.txt           # Python dependencies
├── modules/                   # Core modules
│   ├── __init__.py
│   ├── data_generator.py     # Synthetic data generation
│   ├── ai_predictor.py       # ML-based health risk prediction
│   ├── alert_system.py       # Alert management and notifications
│   ├── chatbot.py            # Interactive health assistant
│   └── real_time_monitor.py  # Real-time vital monitoring
├── data/                      # Health datasets
│   └── health_data.csv
└── models/                    # Trained AI models
    ├── health_predictor.pkl
    └── scaler.pkl
```

## 📊 Health Parameters Monitored

- **Heart Rate** (bpm): Normal range 60-100
- **Blood Pressure** (mmHg): Systolic 90-120, Diastolic 60-80
- **Body Temperature** (°C): Normal range 36.1-37.2
- **Oxygen Saturation** (%): Normal range 95-100
- **Respiratory Rate** (/min): Normal range 12-20

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/praveenbot2/AI_Health_Monitor-.git
cd AI_Health_Monitor-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Setup and Training

Run the setup to generate data and train the AI model:

```bash
python main.py
```

This will:
- Generate a synthetic health dataset (1000 samples)
- Train the Random Forest-based health risk predictor
- Save the trained model for future use

### Usage

#### 1. Command-Line Interface

Run the interactive demo:

```bash
python main.py
```

Choose from:
- Single Health Check: Enter vitals manually for instant assessment
- Real-Time Monitoring: Simulate continuous health monitoring
- Chat with Health Assistant: Ask health-related questions

#### 2. Web API Server

Start the Flask web server:

```bash
python web_server.py
```

The server runs on `http://localhost:5000` with the following endpoints:

**Health Risk Prediction:**
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

**Chatbot Interaction:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a normal heart rate?"}'
```

**Get Simulated Vitals:**
```bash
curl http://localhost:5000/monitor?condition=healthy
```

**Alert Summary:**
```bash
curl http://localhost:5000/alerts
```

#### 3. Individual Modules

Test individual modules:

```bash
# Generate dataset
python modules/data_generator.py

# Train AI model
python modules/ai_predictor.py

# Test alert system
python modules/alert_system.py

# Test chatbot
python modules/chatbot.py

# Run real-time monitoring
python modules/real_time_monitor.py
```

## 🤖 AI Model

The system uses a **Random Forest Classifier** trained on synthetic health data:

- **Input Features**: 6 vital signs (heart rate, blood pressure, temperature, oxygen saturation, respiratory rate)
- **Output**: Health risk classification (Low, Medium, High)
- **Accuracy**: ~95% on test data
- **Training Data**: 1000 synthetic health records with various health conditions

## ⚠️ Alert Levels

- **🚨 CRITICAL**: High health risk detected - Immediate medical attention required
- **⚠️ WARNING**: Moderate health risk - Monitor closely and consult a doctor
- **✓ INFO**: Normal health parameters - Continue healthy lifestyle

## 💬 Chatbot Capabilities

The health assistant chatbot can help with:
- Explaining vital signs and normal ranges
- Providing health tips and advice
- Emergency procedures
- Understanding risk assessment
- General health-related questions

Example interactions:
- "What is a normal heart rate?"
- "Tell me about blood pressure"
- "Give me some health tips"
- "What should I do in an emergency?"

## 🔧 Configuration

Modify `config.py` to customize:
- Alert thresholds
- Health parameter ranges
- Model paths
- Server settings
- Dataset size

## 📝 Example Output

```
--- Check #1 at 14:30:45 ---
Vitals: HR=75.0 bpm, BP=115.0/75.0 mmHg, Temp=36.8°C, SpO2=98.0%, RR=16.0 /min
Risk Assessment: LOW (Confidence: 0.897)
Alert Status: INFO

Session Summary:
  Critical Alerts: 0
  Warning Alerts: 0
  Info Messages: 12
```

## 🛡️ Disclaimer

This is a demonstration system for educational purposes. **It is NOT a medical device** and should not be used for actual medical diagnosis or treatment. Always consult qualified healthcare professionals for medical advice.

## 📄 License

This project is open source and available for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.