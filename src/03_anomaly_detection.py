import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

IN_PATH = Path("data/processed/features.csv")
OUT_PATH = Path("data/processed/scored_anomalies.csv")

# Load features
df = pd.read_csv(IN_PATH)
df["date"] = pd.to_datetime(df["date"])

# Features used for anomaly detection
feature_cols = [
    "log_return",
    "ret_z_7",
    "vol_log_change",
    "volatility_14",
    "drawdown_30"
]

X = df[feature_cols].copy()

# Scale features (important for Isolation Forest)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Isolation Forest model
model = IsolationForest(
    n_estimators=300,
    contamination=0.03,  # ~3% anomalies (realistic)
    random_state=42
)

model.fit(X_scaled)

# Anomaly scores (lower = more abnormal)
df["anomaly_score"] = model.decision_function(X_scaled)

# Flag anomalies
df["is_anomaly"] = model.predict(X_scaled)
df["is_anomaly"] = (df["is_anomaly"] == -1).astype(int)

# Severity levels based on score quantiles
q_low = df.loc[df["is_anomaly"] == 1, "anomaly_score"].quantile(0.33)
q_high = df.loc[df["is_anomaly"] == 1, "anomaly_score"].quantile(0.66)

def severity(score):
    if score <= q_low:
        return "High"
    elif score <= q_high:
        return "Medium"
    else:
        return "Low"

df["severity"] = np.where(
    df["is_anomaly"] == 1,
    df["anomaly_score"].apply(severity),
    "Normal"
)

# find strongest driver per row
abs_features = X.abs()
df["top_driver"] = abs_features.idxmax(axis=1)
df["driver_value"] = abs_features.max(axis=1)

# Save final table for Tableau
df.to_csv(OUT_PATH, index=False)

print(f"Saved {len(df):,} rows to {OUT_PATH}")
print("Anomalies detected:", df["is_anomaly"].sum())
