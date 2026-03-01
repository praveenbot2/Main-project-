"""
AI Health Monitor - Streamlit Dashboard
Interactive health monitoring, prediction, and chatbot interface
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import time

# Ensure modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_generator import DataGenerator
from modules.ai_predictor import HealthPredictor
from modules.alert_system import AlertSystem
from modules.chatbot import HealthChatbot
from modules.real_time_monitor import RealTimeMonitor
from config import HEALTH_PARAMS

# ── Page Config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Health Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    .risk-high { background: #ff4b4b22; border-left: 4px solid #ff4b4b; padding: 1rem; border-radius: 0.5rem; }
    .risk-medium { background: #ffa50022; border-left: 4px solid #ffa500; padding: 1rem; border-radius: 0.5rem; }
    .risk-low { background: #00cc4422; border-left: 4px solid #00cc44; padding: 1rem; border-radius: 0.5rem; }
    .metric-card { background: #f0f2f6; padding: 1rem; border-radius: 0.5rem; text-align: center; }
    div[data-testid="stMetric"] { background: #f8f9fa; padding: 0.75rem; border-radius: 0.5rem; }
</style>
""", unsafe_allow_html=True)


# ── Initialization ───────────────────────────────────────────────────────
@st.cache_resource
def init_system():
    """Initialize all system components (cached across reruns)."""
    # Generate data if missing
    if not os.path.exists("data/health_data.csv"):
        os.makedirs("data", exist_ok=True)
        DataGenerator().save_dataset()

    predictor = HealthPredictor()
    # Train if model doesn't exist
    if not os.path.exists("models/health_predictor.pkl"):
        os.makedirs("models", exist_ok=True)
        predictor.train()
    else:
        predictor.load_model()

    return {
        "predictor": predictor,
        "alert_system": AlertSystem(),
        "chatbot": HealthChatbot(),
        "monitor": RealTimeMonitor(),
    }


components = init_system()

# ── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🏥 AI Health Monitor")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🔍 Health Check", "📊 Real-Time Monitor", "💬 Health Chat", "📋 Alert History", "ℹ️ About"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("AI-Driven Health Monitoring & Alert System")

# ══════════════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════════════

# ── Dashboard ────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.markdown("Welcome to the **AI Health Monitoring System**. Use the sidebar to navigate.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Vitals Tracked", "6", help="Heart rate, BP, temperature, SpO2, respiratory rate")
    col2.metric("ML Model", "Ensemble", help="Random Forest + Gradient Boosting")
    col3.metric("Risk Levels", "3", help="Low, Medium, High")
    col4.metric("Alert Types", "3", help="Info, Warning, Critical")

    st.markdown("---")

    # Quick health check
    st.subheader("⚡ Quick Health Check")
    st.markdown("Enter your vital signs for an instant AI-powered risk assessment.")

    qc1, qc2, qc3 = st.columns(3)
    with qc1:
        q_hr = st.number_input("Heart Rate (bpm)", 40, 200, 75, key="q_hr")
        q_sys = st.number_input("BP Systolic (mmHg)", 70, 200, 115, key="q_sys")
    with qc2:
        q_dia = st.number_input("BP Diastolic (mmHg)", 40, 130, 75, key="q_dia")
        q_temp = st.number_input("Temperature (°C)", 35.0, 42.0, 36.6, step=0.1, key="q_temp")
    with qc3:
        q_o2 = st.number_input("SpO2 (%)", 70, 100, 98, key="q_o2")
        q_rr = st.number_input("Respiratory Rate (/min)", 8, 40, 16, key="q_rr")

    if st.button("🔍 Predict Risk", key="quick_predict", type="primary"):
        vitals = {
            "heart_rate": float(q_hr),
            "blood_pressure_systolic": float(q_sys),
            "blood_pressure_diastolic": float(q_dia),
            "temperature": float(q_temp),
            "oxygen_saturation": float(q_o2),
            "respiratory_rate": float(q_rr),
        }
        result = components["predictor"].predict(vitals)
        alert = components["alert_system"].check_and_alert(result, vitals)

        risk = result["risk_level"].lower()
        css_class = f"risk-{risk}"
        icon = {"high": "🚨", "medium": "⚠️", "low": "✅"}.get(risk, "ℹ️")

        st.markdown(f'<div class="{css_class}"><h3>{icon} Risk Level: {result["risk_level"]}</h3>'
                    f'<p>Confidence: {result["probability"]*100:.1f}%</p></div>',
                    unsafe_allow_html=True)

        if result.get("conditions"):
            st.warning("**Detected Conditions:** " + ", ".join(c["detail"] for c in result["conditions"]))

        st.info("**Recommendations:** " + " • ".join(result["recommendations"]))

    # Dataset overview
    st.markdown("---")
    st.subheader("📊 Training Dataset Overview")
    if os.path.exists("data/health_data.csv"):
        df = pd.read_csv("data/health_data.csv")
        st.dataframe(df.describe().round(2), use_container_width=True)
    else:
        st.info("No dataset found. It will be generated on first prediction.")


# ── Health Check ─────────────────────────────────────────────────────────
elif page == "🔍 Health Check":
    st.title("🔍 Detailed Health Check")
    st.markdown("Enter patient vitals for comprehensive AI analysis.")

    with st.form("health_check_form"):
        st.subheader("Vital Signs Input")
        c1, c2 = st.columns(2)

        with c1:
            hr = st.slider("Heart Rate (bpm)", 40, 200, 75,
                           help=f"Normal: {HEALTH_PARAMS['heart_rate']['normal']}")
            sys_bp = st.slider("BP Systolic (mmHg)", 70, 200, 115,
                               help=f"Normal: {HEALTH_PARAMS['blood_pressure_systolic']['normal']}")
            dia_bp = st.slider("BP Diastolic (mmHg)", 40, 130, 75,
                               help=f"Normal: {HEALTH_PARAMS['blood_pressure_diastolic']['normal']}")

        with c2:
            temp = st.slider("Temperature (°C)", 35.0, 42.0, 36.6, step=0.1,
                             help=f"Normal: {HEALTH_PARAMS['temperature']['normal']}")
            o2 = st.slider("Oxygen Saturation (%)", 70, 100, 98,
                           help=f"Normal: {HEALTH_PARAMS['oxygen_saturation']['normal']}")
            rr = st.slider("Respiratory Rate (/min)", 8, 40, 16,
                           help=f"Normal: {HEALTH_PARAMS['respiratory_rate']['normal']}")

        submitted = st.form_submit_button("🩺 Analyze Health", type="primary")

    if submitted:
        vitals = {
            "heart_rate": float(hr),
            "blood_pressure_systolic": float(sys_bp),
            "blood_pressure_diastolic": float(dia_bp),
            "temperature": float(temp),
            "oxygen_saturation": float(o2),
            "respiratory_rate": float(rr),
        }

        with st.spinner("Analyzing vitals..."):
            result = components["predictor"].predict(vitals)
            alert = components["alert_system"].check_and_alert(result, vitals)

        # Results
        st.markdown("---")
        st.subheader("📊 Analysis Results")

        r1, r2, r3 = st.columns(3)
        risk = result["risk_level"].lower()
        r1.metric("Risk Level", result["risk_level"],
                  delta="Normal" if risk == "low" else "Attention needed",
                  delta_color="normal" if risk == "low" else "inverse")
        r2.metric("Confidence", f"{result['probability']*100:.1f}%")
        r3.metric("Alert Type", alert["alert_type"])

        # Risk probabilities
        st.subheader("Risk Probability Distribution")
        probs = result.get("risk_probabilities", {})
        if probs:
            prob_df = pd.DataFrame({
                "Risk Level": [k.capitalize() for k in probs.keys()],
                "Probability": list(probs.values()),
            })
            st.bar_chart(prob_df.set_index("Risk Level"))

        # Conditions
        if result.get("conditions"):
            st.subheader("⚠️ Detected Conditions")
            for cond in result["conditions"]:
                severity_icon = "🔴" if cond["severity"] == "critical" else "🟡"
                st.markdown(f"{severity_icon} **{cond['name'].replace('_', ' ').title()}** — {cond['detail']}")

        # Recommendations
        st.subheader("💡 Recommendations")
        for rec in result["recommendations"]:
            st.markdown(f"• {rec}")

        # Vital signs summary
        st.subheader("📋 Vital Signs Summary")
        vitals_df = pd.DataFrame([{
            "Parameter": k.replace("_", " ").title(),
            "Value": v,
            "Normal Range": f"{HEALTH_PARAMS[k]['normal'][0]} – {HEALTH_PARAMS[k]['normal'][1]}",
            "Status": "✅ Normal" if HEALTH_PARAMS[k]["normal"][0] <= v <= HEALTH_PARAMS[k]["normal"][1] else "⚠️ Abnormal",
        } for k, v in vitals.items()])
        st.dataframe(vitals_df, use_container_width=True, hide_index=True)


# ── Real-Time Monitor ───────────────────────────────────────────────────
elif page == "📊 Real-Time Monitor":
    st.title("📊 Real-Time Health Monitor")
    st.markdown("Simulate continuous vital sign monitoring with AI risk assessment.")

    mc1, mc2 = st.columns(2)
    with mc1:
        condition = st.selectbox("Simulation Condition", ["healthy", "at_risk", "critical"])
    with mc2:
        n_readings = st.slider("Number of Readings", 5, 30, 10)

    if st.button("▶️ Start Monitoring", type="primary"):
        monitor = components["monitor"]

        chart_placeholder = st.empty()
        metrics_placeholder = st.empty()
        alert_placeholder = st.empty()

        history = []

        progress = st.progress(0)
        for i in range(n_readings):
            vitals = monitor.simulate_vitals(condition)
            result = components["predictor"].predict(vitals)
            alert = components["alert_system"].check_and_alert(result, vitals)

            vitals["reading"] = i + 1
            vitals["risk_level"] = result["risk_level"]
            history.append(vitals)

            df = pd.DataFrame(history)

            # Update charts
            with chart_placeholder.container():
                tab1, tab2, tab3 = st.tabs(["Heart Rate & BP", "Temperature & SpO2", "Respiratory Rate"])
                with tab1:
                    st.line_chart(df.set_index("reading")[["heart_rate", "blood_pressure_systolic", "blood_pressure_diastolic"]])
                with tab2:
                    c1, c2 = st.columns(2)
                    c1.line_chart(df.set_index("reading")[["temperature"]])
                    c2.line_chart(df.set_index("reading")[["oxygen_saturation"]])
                with tab3:
                    st.line_chart(df.set_index("reading")[["respiratory_rate"]])

            # Update metrics
            with metrics_placeholder.container():
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Heart Rate", f"{vitals['heart_rate']} bpm")
                m2.metric("Blood Pressure", f"{vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']}")
                m3.metric("SpO2", f"{vitals['oxygen_saturation']}%")
                m4.metric("Risk", result["risk_level"])

            # Show alert
            with alert_placeholder.container():
                if alert["alert_type"] == "CRITICAL":
                    st.error(alert["message"])
                elif alert["alert_type"] == "WARNING":
                    st.warning(alert["message"])
                else:
                    st.success(alert["message"])

            progress.progress((i + 1) / n_readings)
            time.sleep(0.5)

        st.success(f"Monitoring complete — {n_readings} readings captured.")

        # Summary table
        st.subheader("📋 Monitoring History")
        st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)


# ── Chat ─────────────────────────────────────────────────────────────────
elif page == "💬 Health Chat":
    st.title("💬 Health Assistant Chat")
    st.markdown("Ask questions about health, vitals, symptoms, or wellness tips.")

    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! I'm your AI Health Assistant. Ask me about heart rate, blood pressure, symptoms, or general health tips. How can I help?"}
        ]

    # Display chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask a health question..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = components["chatbot"].process_message(prompt)
            st.markdown(response)

        st.session_state.chat_messages.append({"role": "assistant", "content": response})


# ── Alert History ────────────────────────────────────────────────────────
elif page == "📋 Alert History":
    st.title("📋 Alert History")

    summary = components["alert_system"].get_alert_summary()

    if isinstance(summary, str):
        st.info(summary)
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Alerts", summary["total_alerts"])
        c2.metric("🔴 Critical", summary["critical"])
        c3.metric("🟡 Warning", summary["warning"])
        c4.metric("🟢 Info", summary["info"])

        st.markdown("---")
        st.subheader("Recent Alerts")
        for alert in reversed(summary.get("recent_alerts", [])):
            icon = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🟢"}.get(alert["alert_type"], "⚪")
            with st.expander(f"{icon} {alert['alert_type']} — {alert['timestamp'][:19]}"):
                st.markdown(f"**Message:** {alert['message']}")
                st.markdown(f"**Risk Level:** {alert['risk_level']} ({alert['probability']*100:.1f}%)")
                if alert.get("recommendations"):
                    st.markdown("**Recommendations:**")
                    for rec in alert["recommendations"]:
                        st.markdown(f"  • {rec}")

    if st.button("🗑️ Clear Alert History"):
        components["alert_system"].clear_history()
        st.rerun()


# ── About ────────────────────────────────────────────────────────────────
elif page == "ℹ️ About":
    st.title("ℹ️ About AI Health Monitor")

    st.markdown("""
    ### AI-Driven Health Monitoring and Alert System

    This system uses machine learning to monitor vital signs, predict health risks,
    and provide intelligent alerts and recommendations.

    ---

    #### Features
    - **AI Risk Prediction** — Ensemble model (Random Forest + Gradient Boosting) with ~98% accuracy
    - **Real-Time Monitoring** — Continuous vital sign simulation and tracking
    - **Smart Alerts** — 3-tier alert system (Critical, Warning, Info)
    - **Health Chatbot** — NLP-powered assistant with medical knowledge base
    - **Data Visualization** — Interactive charts and trend analysis

    ---

    #### Vital Signs Monitored
    | Parameter | Normal Range |
    |-----------|-------------|
    | Heart Rate | 60–100 bpm |
    | BP Systolic | 90–120 mmHg |
    | BP Diastolic | 60–80 mmHg |
    | Temperature | 36.1–37.2°C |
    | SpO2 | 95–100% |
    | Respiratory Rate | 12–20 /min |

    ---

    #### Tech Stack
    - **ML**: scikit-learn (Ensemble classifiers)
    - **Data**: pandas, numpy
    - **UI**: Streamlit
    - **NLP**: TF-IDF intent matching

    ---

    *Built with ❤️ for better health outcomes*
    """)

    # Model info
    metrics = components["predictor"].get_metrics()
    if metrics:
        st.markdown("---")
        st.subheader("🤖 Current Model Metrics")
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Accuracy", f"{metrics['accuracy']*100:.1f}%")
        mc2.metric("Precision", f"{metrics['precision']*100:.1f}%")
        mc3.metric("Recall", f"{metrics['recall']*100:.1f}%")
        mc4.metric("F1 Score", f"{metrics['f1_score']*100:.1f}%")
