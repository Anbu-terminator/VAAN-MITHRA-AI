import os
import sys
import subprocess

def run(cmd):
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("❌ Command failed, stopping execution.")
        sys.exit(1)

print("🚀 Starting Vaan Mithra – Full System Boot")

# Ensure working directory is project root
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1️⃣ Install dependencies
run("pip install -r requirements.txt")

# 2️⃣ Download NASA POWER data
run("python training/download_nasa_power.py")

# 3️⃣ Train NDVI model
run("python training/train_ndvi_model.py")

# 4️⃣ Train Climate model
run("python training/train_climate_model.py")

# 5️⃣ Launch Streamlit app
print("\n🌐 Launching Web App...")
run("streamlit run ai_webapp/app.py")
