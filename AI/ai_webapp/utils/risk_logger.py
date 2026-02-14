import pandas as pd
import os
from datetime import datetime

LOG_PATH = "ai_webapp/utils/risk_log.csv"

def log_risk(temp, risk):
    row = {
        "time": datetime.now(),
        "temperature": temp,
        "risk": risk
    }

    if os.path.exists(LOG_PATH):
        df = pd.read_csv(LOG_PATH)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(LOG_PATH, index=False)
