import sys, os
sys.path.append(os.path.abspath("."))

import streamlit as st
import numpy as np
import joblib
from PIL import Image
import matplotlib.pyplot as plt

from alerts.tamil_voice import tamil_voice_alert
from alerts.telegram_alert import telegram_alert
from ai_webapp.utils.location_utils import format_location

MODEL_PATH = "ai_webapp/models/ndvi_image_model.pkl"

st.title("🌱 NDVI Analysis & Crop Health Alert")

# ---------------- MODEL CHECK ----------------
if not os.path.exists(MODEL_PATH):
    st.error("❌ NDVI model not found. Run training first.")
    st.stop()

model = joblib.load(MODEL_PATH)

# ---------------- LOCATION INPUT ----------------
st.subheader("📍 Farmer Location")
lat = st.number_input("Latitude", value=11.0)
lon = st.number_input("Longitude", value=78.0)
location_name = format_location(lat, lon)

# ---------------- IMAGE UPLOAD ----------------
rgb_file = st.file_uploader("Upload RGB Image", ["jpg", "png"])
nir_file = st.file_uploader("Upload NIR Image", ["jpg", "png"])

if rgb_file and nir_file:
    rgb_img = Image.open(rgb_file).convert("L")
    nir_img = Image.open(nir_file).convert("L")

    # ✅ Resize to same shape (critical)
    nir_img = nir_img.resize(rgb_img.size)

    rgb = np.array(rgb_img, dtype=np.float32)
    nir = np.array(nir_img, dtype=np.float32)

    # ---------------- NDVI ----------------
    ndvi = (nir - rgb) / (nir + rgb + 1e-6)
    ndvi_mean = float(np.mean(ndvi))

    risk = int(model.predict([[ndvi_mean]])[0])

    # ---------------- DISPLAY SCORE ----------------
    st.metric("🌱 Mean NDVI Value", round(ndvi_mean, 3))
    st.caption(f"Location: {location_name}")

    # ---------------- NDVI IMAGE ----------------
    st.subheader("🛰️ NDVI Processed Image")

    fig, ax = plt.subplots()
    ndvi_plot = ax.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
    plt.colorbar(ndvi_plot, ax=ax, fraction=0.046)
    ax.set_title("NDVI Heatmap")
    ax.axis("off")

    st.pyplot(fig)

    # ---------------- ALERT ----------------
    if risk == 1:
        st.error("🚨 CROP STRESS DETECTED (LOW NDVI)")

        # 🔔 Auto Alerts
        tamil_voice_alert()
        telegram_alert(
            f"🚨 NDVI ALERT\n"
            f"Location: {location_name}\n"
            f"NDVI: {round(ndvi_mean,3)}\n"
            f"Crop stress detected"
        )
    else:
        st.success("✅ Crop Health Normal")
