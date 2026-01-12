import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = Path("data/raw/btc_usd_daily.csv")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_PATH)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# --- Core KPI: log return ---
df["log_close"] = np.log(df["close"])
df["log_return"] = df["log_close"].diff()

# --- Volume features ---
df["vol_log"] = np.log(df["volume"].replace(0, np.nan))
df["vol_log_change"] = df["vol_log"].diff()

# --- Rolling risk features (choose windows that make sense for daily data) ---
w7, w14, w30 = 7, 14, 30

df["ret_mean_7"] = df["log_return"].rolling(w7).mean()
df["ret_std_7"] = df["log_return"].rolling(w7).std()
df["ret_z_7"] = (df["log_return"] - df["ret_mean_7"]) / df["ret_std_7"]

df["volatility_14"] = df["log_return"].rolling(w14).std()
df["volatility_30"] = df["log_return"].rolling(w30).std()

# --- Drawdown (risk / crash indicator) ---
df["rolling_max_30"] = df["close"].rolling(w30).max()
df["drawdown_30"] = (df["close"] / df["rolling_max_30"]) - 1

# Keep only columns we need for modeling + Tableau
features = df[[
    "date", "close", "volume",
    "log_return", "ret_z_7",
    "vol_log_change",
    "volatility_14", "volatility_30",
    "drawdown_30"
]].copy()

# Drop early rows with NaNs caused by rolling windows / diff
features = features.dropna().reset_index(drop=True)

out_path = OUT_DIR / "features.csv"
features.to_csv(out_path, index=False)

print(f"Saved {len(features):,} rows to {out_path}")
print("Columns:", list(features.columns))
