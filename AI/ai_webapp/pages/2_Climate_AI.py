import sys, os
sys.path.append(os.path.abspath("."))

import streamlit as st
import requests
import joblib
import pandas as pd

from qrng.qrng_entropy import qrng_entropy
from alerts.tamil_voice import tamil_voice_alert
from alerts.telegram_alert import telegram_alert
from ai_webapp.utils.risk_logger import log_risk
from ai_webapp.utils.risk_charts import show_risk_charts

# ---------------- CONFIG ----------------
MODEL_PATH = "ai_webapp/models/climate_model.pkl"

CHANNEL_ID = "3246120"
READ_API_KEY = "482OXGTKAOAF90EB"

st.title("🌦️ Climate AI – Real Sensor Based")

# ---------------- LOAD MODEL ----------------
if not os.path.exists(MODEL_PATH):
    st.error("❌ Climate model not found. Train it first.")
    st.stop()

model = joblib.load(MODEL_PATH)

# ---------------- SAFE FLOAT (CRITICAL FIX) ----------------
def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default

# ---------------- THINGSPEAK DATA (NULL-SAFE) ----------------
def get_thingspeak_data():
    url = (
        f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json"
        f"?api_key={READ_API_KEY}"
    )

    data = requests.get(url, timeout=10).json()

    sensor_data = {
        "temperature": safe_float(data.get("field1")),
        "humidity": safe_float(data.get("field2")),
        "gas": safe_float(data.get("field3")),
        "uv": safe_float(data.get("field4")),
        "altitude": safe_float(data.get("field5")),
    }

    return sensor_data

# ---------------- WEATHER API ----------------
def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=11.0&longitude=78.0&current_weather=true"
    )
    return requests.get(url, timeout=10).json()["current_weather"]

# ---------------- RUN AI ----------------
if st.button("Run Climate Risk Analysis"):
    try:
        sensor = get_thingspeak_data()
        weather = get_weather()
        entropy = qrng_entropy()

        # ---------------- FEATURE FUSION ----------------
        X = pd.DataFrame(
            [[
                weather["temperature"],  # Weather temperature
                0.0                       # Rain proxy (matches training)
            ]],
            columns=["T2M", "RAIN"]
        )

        risk = int(model.predict(X)[0])

        # ---------------- LOGGING ----------------
        log_risk(weather["temperature"], risk)

        # ---------------- DISPLAY ----------------
        st.subheader("📡 Live Sensor Data (ThingSpeak)")
        st.write(sensor)

        # Warn if any sensor value missing
        for k, v in sensor.items():
            if v == 0.0:
                st.warning(f"⚠️ {k.capitalize()} data missing or not updated yet")

        st.subheader("🌤️ Live Weather Data")
        st.write(weather)

        st.metric("QRNG Entropy", round(entropy, 4))

        if risk == 1:
            st.error("🚨 HIGH CLIMATE RISK DETECTED")

            # 🔔 AUTO ALERTS
            tamil_voice_alert()
            telegram_alert(
                f"🚨 CLIMATE ALERT\n"
                f"Temp: {weather['temperature']}°C\n"
                f"Humidity: {sensor['humidity']}%\n"
                f"Gas: {sensor['gas']}\n"
                f"UV: {sensor['uv']}\n"
                f"Altitude: {sensor['altitude']}"
            )
        else:
            st.success("✅ Climate Conditions Safe")

    except Exception as e:
        st.exception(e)

# ---------------- RISK TRENDS ----------------
st.divider()
show_risk_charts()
