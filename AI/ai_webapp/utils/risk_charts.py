import pandas as pd
import streamlit as st
import os

LOG_PATH = "ai_webapp/utils/risk_log.csv"

def show_risk_charts():
    if not os.path.exists(LOG_PATH):
        st.info("No risk history yet")
        return

    df = pd.read_csv(LOG_PATH)
    df["time"] = pd.to_datetime(df["time"])

    st.subheader("📊 Risk Trend Over Time")
    st.line_chart(df.set_index("time")[["risk"]])

    st.subheader("🌡️ Temperature Trend")
    st.line_chart(df.set_index("time")[["temperature"]])
