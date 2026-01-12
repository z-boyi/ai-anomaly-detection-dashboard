import yfinance as yf
import pandas as pd
from pathlib import Path

# Output directory
OUT_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Yahoo Finance ticker for Bitcoin
TICKER = "BTC-USD"

# Download daily data
df = yf.download(
    TICKER,
    period="max",
    interval="1d",
    auto_adjust=False,
    progress=False
)

# Clean column names
df = df.reset_index()

# Reset index so date becomes a column
df = df.reset_index()

# Handle MultiIndex columns safely
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [c[0] for c in df.columns]

# Normalize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")


# Keep only relevant columns
df = df[["date", "close", "volume"]].dropna()

# Save to CSV
output_path = OUT_DIR / "btc_usd_daily.csv"
df.to_csv(output_path, index=False)

print(f"Saved {len(df):,} rows to {output_path}")
