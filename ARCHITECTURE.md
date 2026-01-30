# System Architecture

## AI-Driven Health Monitoring and Alert System

### Overview
This document describes the architecture and component interactions of the AI Health Monitor system.

## System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                   AI HEALTH MONITOR SYSTEM                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  • Command-Line Interface (main.py)                             │
│  • Web API Server (web_server.py) - Flask REST API             │
│  • Demo Scripts (demo.py)                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │  Real-Time       │  │  Alert System    │                   │
│  │  Monitor         │→ │  - Notifications │                   │
│  │  - Continuous    │  │  - Alert Levels  │                   │
│  │    Monitoring    │  │  - History       │                   │
│  └──────────────────┘  └──────────────────┘                   │
│           ↓                      ↑                              │
│  ┌──────────────────┐           │                              │
│  │  AI Predictor    │───────────┘                              │
│  │  - Random Forest │                                           │
│  │  - Risk Predict  │                                           │
│  │  - 98.5% Acc     │                                           │
│  └──────────────────┘                                           │
│           ↓                                                      │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │  Chatbot         │  │  Data Generator  │                   │
│  │  - Health Q&A    │  │  - Synthetic     │                   │
│  │  - Interactive   │  │    Data          │                   │
│  └──────────────────┘  └──────────────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                   │
├─────────────────────────────────────────────────────────────────┤
│  • Trained Models (models/*.pkl)                                │
│  • Health Dataset (data/health_data.csv)                        │
│  • Configuration (config.py)                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Training Phase
```
Data Generator → CSV Dataset → AI Predictor → Trained Model
```

### 2. Prediction Phase
```
User Input → AI Predictor → Risk Assessment → Alert System
                                                    ↓
                                             Notifications
```

### 3. Monitoring Phase
```
Simulate/Sensors → Real-Time Monitor → AI Predictor → Alerts
                         ↓
                   History Storage
```

### 4. Chatbot Interaction
```
User Query → Chatbot → Intent Recognition → Response
                 ↓
          Conversation History
```

## Component Details

### 1. Data Generator Module
- **Purpose**: Generate synthetic health monitoring data
- **Output**: CSV file with health records
- **Features**:
  - 6 vital sign parameters
  - Multiple health conditions (healthy, at-risk, critical)
  - Realistic distributions

### 2. AI Predictor Module
- **Algorithm**: Random Forest Classifier
- **Input**: 6 vital signs
  - Heart Rate
  - Blood Pressure (Systolic/Diastolic)
  - Body Temperature
  - Oxygen Saturation
  - Respiratory Rate
- **Output**: Risk level (Low/Medium/High) + Probability + Recommendations
- **Performance**: 98.5% accuracy

### 3. Alert System Module
- **Purpose**: Generate and manage health alerts
- **Alert Levels**:
  - 🚨 CRITICAL: Immediate medical attention required
  - ⚠️ WARNING: Consult doctor soon
  - ✓ INFO: Normal parameters
- **Features**:
  - Alert history tracking
  - Notification triggering
  - Summary statistics

### 4. Chatbot Module
- **Purpose**: Interactive health assistant
- **Capabilities**:
  - Explain vital signs
  - Provide health tips
  - Answer health queries
  - Emergency guidance
- **Technology**: Rule-based NLP with keyword matching

### 5. Real-Time Monitor Module
- **Purpose**: Continuous health monitoring
- **Features**:
  - Configurable monitoring intervals
  - Multiple condition simulations
  - Session history
  - Integration with AI predictor and alert system

## API Endpoints

### Web Server (Flask)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | System health check |
| `/predict` | POST | Predict health risk from vitals |
| `/chat` | POST | Interact with chatbot |
| `/monitor` | GET | Get simulated vitals |
| `/alerts` | GET | Get alert summary |
| `/simulate` | POST | Simulate monitoring check |

## Technology Stack

- **Language**: Python 3.8+
- **ML Framework**: scikit-learn
- **Web Framework**: Flask
- **Data Processing**: pandas, numpy
- **Model Persistence**: joblib

## Configuration

Centralized configuration in `config.py`:
- Model paths
- Alert thresholds
- Health parameter ranges
- Server settings
- Dataset parameters

## Deployment Architecture

```
┌─────────────┐      HTTP      ┌──────────────┐
│   Clients   │ ────────────→  │ Flask Server │
│  (API/CLI)  │                │ (Port 5000)  │
└─────────────┘                └──────────────┘
                                      ↓
                               ┌──────────────┐
                               │   Modules    │
                               │   Layer      │
                               └──────────────┘
                                      ↓
                               ┌──────────────┐
                               │   Models &   │
                               │     Data     │
                               └──────────────┘
```

## Security Considerations

1. **Input Validation**: All user inputs are validated
2. **Model Security**: Trained models stored securely
3. **API Security**: Add authentication in production
4. **Data Privacy**: Sensitive health data handling
5. **Error Handling**: Graceful error management

## Scalability

### Current Design
- Single-instance deployment
- In-memory processing
- File-based model storage

### Future Enhancements
- Database integration for persistent storage
- Load balancing for multiple instances
- Caching layer for faster predictions
- Message queue for async processing
- Cloud deployment (AWS/Azure/GCP)

## Monitoring & Logging

Current implementation includes:
- Console logging
- Error tracking
- Alert history
- Monitoring session records

Future additions:
- Centralized logging (ELK stack)
- Performance metrics
- System health monitoring
- Usage analytics

## Testing Strategy

1. **Unit Tests**: Individual module testing
2. **Integration Tests**: Component interaction tests
3. **API Tests**: Web server endpoint testing
4. **Demo Scripts**: End-to-end validation

## Maintenance

### Regular Tasks
- Model retraining with new data
- Alert threshold tuning
- Performance monitoring
- Security updates

### Version Control
- Git-based version control
- Branch-based development
- Code review process

## Documentation

- README.md: Project overview and quick start
- USAGE_GUIDE.md: Detailed usage instructions
- ARCHITECTURE.md: System architecture (this file)
- Code comments: Inline documentation

## Conclusion

The AI Health Monitor system provides a complete, modular solution for real-time health monitoring with AI-powered risk assessment, intelligent alerting, and interactive assistance through a chatbot interface.
