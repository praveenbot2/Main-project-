# 🏥 AI-Driven Health Monitoring and Alert System

A real-time health monitoring system powered by machine learning that tracks vital signs, predicts health risks, generates intelligent alerts, and provides an interactive health assistant chatbot — all through a Streamlit dashboard.

## 🌟 Features

- **AI Risk Prediction** — Ensemble ML model (Random Forest + Gradient Boosting) with ~98% accuracy
- **Real-Time Monitoring** — Continuous vital sign simulation with live charts
- **Smart Alerts** — 3-tier alert system (Critical, Warning, Info)
- **Health Chatbot** — NLP-powered assistant with medical knowledge base
- **Interactive Dashboard** — Clean Streamlit UI with data visualization

## 📊 Vital Signs Monitored

| Parameter | Normal Range |
|-----------|-------------|
| Heart Rate | 60–100 bpm |
| BP Systolic | 90–120 mmHg |
| BP Diastolic | 60–80 mmHg |
| Temperature | 36.1–37.2°C |
| SpO2 | 95–100% |
| Respiratory Rate | 12–20 /min |

## 🏗️ Project Structure

```
AI_Health_Monitor/
├── streamlit_app.py           # Streamlit dashboard (main entry)
├── config.py                  # Configuration settings
├── main.py                    # CLI entry point
├── demo.py                    # Feature demo script
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit config
├── modules/                   # Core ML & logic modules
│   ├── ai_predictor.py        # Ensemble ML health risk predictor
│   ├── alert_system.py        # Alert generation & management
│   ├── anomaly_detector.py    # Isolation Forest anomaly detection
│   ├── chatbot.py             # Health chatbot interface
│   ├── data_generator.py      # Synthetic health data generator
│   ├── forecaster.py          # Vital sign trend forecasting
│   ├── real_time_monitor.py   # Real-time monitoring simulation
│   └── smart_chatbot.py       # NLP-powered smart chatbot
├── data/                      # Generated datasets (auto-created)
└── models/                    # Trained model artifacts (auto-created)
```

## 🚀 Quick Start

### Local Setup

```bash
git clone https://github.com/praveenbot2/AI_Health_Monitor-.git
cd AI_Health_Monitor-
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app will auto-generate training data and train the ML model on first launch.

### CLI Mode

```bash
python main.py
```

### Demo

```bash
python demo.py
```

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `streamlit_app.py`
5. Click **Deploy**

The app auto-generates data and trains the model on first run — no manual setup needed.

## 🤖 AI Model

- **Algorithm**: Ensemble (Random Forest + Gradient Boosting with soft voting)
- **Features**: 6 raw vitals + 4 derived features (pulse pressure, MAP, temp deviation, O2 deficit)
- **Output**: Risk classification (Low / Medium / High) with confidence scores
- **Accuracy**: ~98% on test data

## ⚠️ Alert Levels

- 🚨 **CRITICAL** — High health risk, immediate attention required
- ⚠️ **WARNING** — Moderate risk, monitor closely
- ✅ **INFO** — Normal parameters

## 🛡️ Disclaimer

This is a **demonstration system for educational purposes**. It is NOT a medical device and should not be used for actual medical diagnosis or treatment. Always consult qualified healthcare professionals.

## 📄 License

Open source — available for educational and research purposes.# AI-Driven-Health-Monitoring-and-Alert-System
# AI-Driven-Health-Monitoring-and-Alert-System
