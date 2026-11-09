"""Sanity-check detected anomalies against well-known BTC market events.

For each event, report whether the model flagged at least one anomaly
within a +/- WINDOW_DAYS window around the event date.
"""
import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/scored_anomalies.csv")
OUT_PATH = Path("data/processed/event_validation.csv")
WINDOW_DAYS = 3

EVENTS = [
    ("2015-01-14", "Early-2015 crash (Bitstamp hack period)"),
    ("2017-12-17", "2017 bubble peak"),
    ("2018-11-20", "Nov 2018 sell-off (BCH hard fork)"),
    ("2020-03-12", "COVID-19 'Black Thursday' crash"),
    ("2021-05-19", "May 2021 China mining crackdown crash"),
    ("2022-05-09", "Terra/LUNA collapse"),
    ("2022-06-13", "Celsius freeze / 3AC contagion"),
    ("2022-11-08", "FTX collapse"),
    ("2024-08-05", "Aug 2024 global market sell-off (yen carry unwind)"),
]

df = pd.read_csv(IN_PATH, parse_dates=["date"])
anoms = df[df["is_anomaly"] == 1]

rows = []
for date_str, name in EVENTS:
    d = pd.Timestamp(date_str)
    window = anoms[(anoms["date"] - d).abs() <= pd.Timedelta(days=WINDOW_DAYS)]
    hit = not window.empty
    top = window.sort_values("anomaly_score").iloc[0] if hit else None
    rows.append({
        "event_date": date_str,
        "event": name,
        "detected": hit,
        "flag_date": top["date"].date() if hit else None,
        "severity": top["severity"] if hit else None,
        "top_driver": top["top_driver"] if hit else None,
    })

result = pd.DataFrame(rows)
result.to_csv(OUT_PATH, index=False)

print(result.to_string(index=False))
print(f"\nDetected {result['detected'].sum()}/{len(result)} events "
      f"(window = +/-{WINDOW_DAYS} days)")
print(f"Anomaly rate: {len(anoms)}/{len(df)} days = {len(anoms)/len(df):.1%}")
