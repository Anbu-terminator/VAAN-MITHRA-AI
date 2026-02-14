import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

CSV_PATH = "datasets/ndvi/vegetation_indices.csv"
MODEL_PATH = "ai_webapp/models/ndvi_image_model.pkl"

print("🔄 Starting NDVI model training...")

# ---------- CHECK DATASET ----------
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"❌ NDVI dataset not found at {CSV_PATH}")

data = pd.read_csv(CSV_PATH)

# ---------- FIND NDVI COLUMN ----------
ndvi_cols = [c for c in data.columns if "ndvi" in c.lower()]
if not ndvi_cols:
    raise ValueError("❌ No NDVI column found in the dataset")

ndvi_col = ndvi_cols[0]
print(f"✅ Using NDVI column: {ndvi_col}")

# ---------- TRAINING DATA ----------
X = data[[ndvi_col]]
y = (data[ndvi_col] < 0.3).astype(int)  # stress threshold

# ---------- TRAIN MODEL ----------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X, y)

# ---------- SAVE MODEL ----------
os.makedirs("ai_webapp/models", exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("✅ NDVI model trained successfully")
print(f"📦 Model saved at: {MODEL_PATH}")
