import streamlit as st
import numpy as np
import pandas as pd
from src.feedback_system import RangeFeedback
from src.soh_updater import SoHUpdater
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="EV Range Prediction Dashboard",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🔋 Adaptive, Uncertainty-Aware EV Range Prediction")
st.markdown("### Intelligent Range Estimation Based on Driving & Environmental Factors")

# Initialize feedback + SoH models
feedback_engine = RangeFeedback()
soh_engine = SoHUpdater(initial_soh=0.92)

# -----------------------------
# USER INPUTS
# -----------------------------
st.sidebar.header("Vehicle & Trip Parameters")

speed = st.sidebar.slider("Average Speed (km/h)", 20, 120, 60)
traffic = st.sidebar.slider("Traffic Level (0=Low, 1=High)", 0.0, 1.0, 0.4)
temperature = st.sidebar.slider("Outside Temperature (°C)", -10, 45, 28)
load = st.sidebar.slider("Load Weight (kg)", 0, 500, 150)
battery_age = st.sidebar.slider("Battery Age (years)", 0, 10, 2)
tire_pressure = st.sidebar.slider("Tire Pressure (psi)", 25, 40, 34)
hvac_on = st.sidebar.checkbox("HVAC Active (A/C, Heater)", value=True)
soc = st.sidebar.slider("State of Charge (%)", 0, 100, 75)

# -----------------------------
# SIMULATED MODEL LOGIC (Demo)
# -----------------------------
# Normally you'd load your trained model here and predict.
# For demo, let's generate mock ranges with noise.
base_range = 400
traffic_factor = (1 - traffic * 0.25)
temp_factor = 1 - max(0, (abs(temperature - 25) / 100))
load_factor = 1 - (load / 2000)
battery_factor = 1 - (battery_age * 0.015)
pressure_factor = 1 - abs(34 - tire_pressure) / 100
hvac_factor = 0.95 if hvac_on else 1.0
soh = soh_engine.soh

predicted_range = base_range * traffic_factor * temp_factor * load_factor * battery_factor * pressure_factor * hvac_factor * soh * (soc / 100)
noise = random.uniform(-10, 10)

range_expected = predicted_range + noise
range_safe = range_expected - 20
range_optimistic = range_expected + 20

# -----------------------------
# DISPLAY RESULTS
# -----------------------------
st.subheader("Predicted Range Results")
col1, col2, col3 = st.columns(3)
col1.metric("🔵 Safe Range (km)", f"{range_safe:.1f}")
col2.metric("🟢 Expected Range (km)", f"{range_expected:.1f}")
col3.metric("🟡 Optimistic Range (km)", f"{range_optimistic:.1f}")

# -----------------------------
# FEEDBACK SYSTEM
# -----------------------------
message = feedback_engine.generate_message(
    range_safe, range_expected, range_optimistic,
    traffic_index=traffic,
    hvac_on=hvac_on,
    soh=soh,
    soc=soc
)

st.markdown("### 💬 AI Feedback")
st.info(message)

# -----------------------------
# BATTERY HEALTH
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Battery SoH (Health):** {soh * 100:.2f}%")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("⚙️ Developed as Phase 1 of AI-Based EV Range Prediction & Range Anxiety Reduction System")
