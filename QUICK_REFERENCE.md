# Quick Reference Card

## AI Health Monitor - Command Quick Reference

### Installation & Setup
```bash
# Install dependencies
pip install -r requirements.txt

# First-time setup (generate data & train model)
python main.py
```

### Running the System

#### Command-Line Interface
```bash
# Interactive demo with menu
python main.py

# Run complete demo
python demo.py
```

#### Web API Server
```bash
# Start server on localhost:5000
python web_server.py
```

### Individual Modules

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

### API Quick Reference

#### Base URL
```
http://localhost:5000
```

#### Endpoints

**1. Health Check**
```bash
curl http://localhost:5000/health
```

**2. Predict Risk**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"heart_rate":75,"blood_pressure_systolic":120,"blood_pressure_diastolic":80,"temperature":36.8,"oxygen_saturation":98,"respiratory_rate":16}'
```

**3. Chat**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is a normal heart rate?"}'
```

**4. Monitor Vitals**
```bash
curl "http://localhost:5000/monitor?condition=healthy"
```

**5. Get Alerts**
```bash
curl http://localhost:5000/alerts
```

**6. Simulate Check**
```bash
curl -X POST http://localhost:5000/simulate \
  -H "Content-Type: application/json" \
  -d '{"condition":"healthy"}'
```

### Python Code Snippets

#### Make a Prediction
```python
from modules.ai_predictor import HealthPredictor

predictor = HealthPredictor()
predictor.load_model()

vitals = {
    'heart_rate': 75.0,
    'blood_pressure_systolic': 120.0,
    'blood_pressure_diastolic': 80.0,
    'temperature': 36.8,
    'oxygen_saturation': 98.0,
    'respiratory_rate': 16.0
}

result = predictor.predict(vitals)
print(f"Risk: {result['risk_level']}")
```

#### Chat with Bot
```python
from modules.chatbot import HealthChatbot

chatbot = HealthChatbot()
response = chatbot.process_message("What is a normal heart rate?")
print(response)
```

#### Start Monitoring
```python
from modules.real_time_monitor import RealTimeMonitor

monitor = RealTimeMonitor()
monitor.continuous_monitor(
    duration_seconds=60,
    interval_seconds=5,
    condition='healthy'
)
```

### Health Parameters

| Parameter | Normal Range | Unit |
|-----------|--------------|------|
| Heart Rate | 60-100 | bpm |
| Blood Pressure (Sys) | 90-120 | mmHg |
| Blood Pressure (Dia) | 60-80 | mmHg |
| Temperature | 36.1-37.2 | °C |
| Oxygen Saturation | 95-100 | % |
| Respiratory Rate | 12-20 | /min |

### Risk Levels

| Level | Symbol | Meaning |
|-------|--------|---------|
| Low | ✓ | Normal parameters |
| Medium | ⚠️ | Monitor closely, consult doctor |
| High | 🚨 | Immediate medical attention |

### File Structure
```
AI_Health_Monitor/
├── main.py              # Main application
├── web_server.py        # Flask API server
├── demo.py              # Demo script
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── modules/             # Core modules
│   ├── data_generator.py
│   ├── ai_predictor.py
│   ├── alert_system.py
│   ├── chatbot.py
│   └── real_time_monitor.py
├── data/                # Datasets
├── models/              # Trained models
├── README.md            # Overview
├── USAGE_GUIDE.md       # Detailed guide
└── ARCHITECTURE.md      # System design
```

### Common Issues

**Model not found?**
```bash
python modules/ai_predictor.py
```

**Import errors?**
```bash
pip install -r requirements.txt
```

**Port in use?**
Change in `config.py`:
```python
PORT = 5001
```

### Configuration Options

Edit `config.py` to customize:
- Alert thresholds
- Health parameter ranges
- Server host and port
- Dataset size
- Model paths

### Testing

```bash
# Test API (server must be running)
python test_api.py

# Run demo
python demo.py
```

### Getting Help

- README.md - Project overview
- USAGE_GUIDE.md - Detailed instructions
- ARCHITECTURE.md - System design
- GitHub Issues - Report problems

---
**Disclaimer**: This is a demonstration system for educational purposes only. NOT for medical diagnosis.
