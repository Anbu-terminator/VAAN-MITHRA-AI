import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

CSV_PATH = "datasets/climate/nasa_power.csv"
MODEL_PATH = "ai_webapp/models/climate_model.pkl"

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError("❌ Run download_nasa_power.py first")

data = pd.read_csv(CSV_PATH)

# Training features
X = data[["T2M", "RAIN"]]

# Risk logic (example)
y = ((data["T2M"] > 35) | (data["RAIN"] < 1)).astype(int)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X, y)

os.makedirs("ai_webapp/models", exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("✅ Climate model trained using NASA POWER data")
