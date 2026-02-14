import requests
import pandas as pd
import os
import sys

URL = (
    "https://power.larc.nasa.gov/api/temporal/daily/point?"
    "parameters=T2M,PRECTOTCORR"
    "&community=RE"
    "&latitude=11.0"
    "&longitude=78.0"
    "&start=20180101"
    "&end=20231231"
    "&format=JSON"
)

print("🔄 Downloading NASA POWER data...")

resp = requests.get(URL, timeout=30)

if resp.status_code != 200:
    print("❌ HTTP Error:", resp.status_code)
    print(resp.text)
    sys.exit(1)

data = resp.json()

if "properties" not in data or "parameter" not in data["properties"]:
    print("❌ Unexpected NASA POWER response")
    print(data)
    sys.exit(1)

params = data["properties"]["parameter"]

# ---- SAFELY HANDLE MISSING RAIN ----
temperature = list(params["T2M"].values())
rainfall = list(params.get("PRECTOTCORR", {}).values())

# If rainfall missing, fill zeros
if len(rainfall) == 0:
    rainfall = [0.0] * len(temperature)

os.makedirs("datasets/climate", exist_ok=True)

df = pd.DataFrame({
    "T2M": temperature,
    "RAIN": rainfall
})

df.to_csv("datasets/climate/nasa_power.csv", index=False)

print("✅ NASA POWER dataset saved → datasets/climate/nasa_power.csv")
