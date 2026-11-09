# AI Early-Warning Anomaly Detection Dashboard

## Overview
This project builds an **AI-assisted early-warning monitoring system** for volatile time-series data using **unsupervised learning**.  
An Isolation Forest model is applied to Bitcoin (BTC-USD) market data to automatically detect abnormal behavior, and results are presented through an interactive **Tableau dashboard** for decision-making and risk monitoring.

The focus of this project is **monitoring and anomaly detection**, not trading or prediction.

---

## Live Dashboard
🔗 **Tableau Public:**  
https://public.tableau.com/app/profile/boyi.zhang/viz/Book1_17681887578700/AIEarly-WarningAnomalyDetectionDashboard?publish=yes

---

## Problem Statement
Volatile systems (financial markets, platforms, transactions, infrastructure metrics) require **early detection of abnormal behavior** to support:
- Risk monitoring
- Operational awareness
- Investigative workflows

This project answers:
> *How can we automatically flag unusual patterns in a volatile time-series and surface them in a decision-ready dashboard?*

---

## Data
- **Source:** Yahoo Finance  
- **Asset:** BTC-USD (Bitcoin, daily frequency)
- **Time span:** ~2014 – present
- **Fields used:** Close price, volume

---

## Feature Engineering
Time-series features were engineered to capture risk and abnormal behavior:

- Log returns
- Rolling volatility (14-day, 30-day)
- Rolling z-scores
- Log volume change
- Drawdown from rolling maximum

These features allow the model to detect anomalies driven by **price shocks, volatility spikes, and drawdowns**.

---

## Anomaly Detection Model
- **Model:** Isolation Forest
- **Type:** Unsupervised learning
- **Contamination:** ~3% (realistic anomaly rate)
- **Scaling:** Standardized features

### Outputs
For each date, the model produces:
- Anomaly score
- Anomaly flag (normal vs anomalous)
- Severity level (Low / Medium / High)
- Primary contributing feature (explainability)

This mirrors how anomaly detection is used in **fintech, risk, and monitoring systems**.

---

## Dashboard Design (Tableau)
The Tableau dashboard provides:

- **KPI tiles**
  - Total anomalies detected
  - High-severity anomalies
  - Most recent anomaly date
- **Time-series visualization**
  - BTC price with AI-detected anomalies highlighted
- **Interactivity**
  - Date filtering
  - Severity filtering
  - Hover tooltips with anomaly explanations

The dashboard is designed for **exploration, monitoring, and communication**, not model training.

---
## Project Structure
```
.
├── data
│   ├── processed
│   │   ├── features.csv
│   │   └── scored_anomalies.csv
│   └── raw
│       └── btc_usd_daily.csv
├── images
│   └── AI Early-Warning Anomaly Detection Dashboard.png
├── README.md
├── requirements.txt
└── src
    ├── 01_download_btc.py
    ├── 02_build_features.py
    ├── 03_anomaly_detection.py
    └── 04_validate_events.py
```

### How to Run
```bash
pip install -r requirements.txt
python src/01_download_btc.py
python src/02_build_features.py
python src/03_anomaly_detection.py
python src/04_validate_events.py
```

---

## Validation Against Known Market Events
There are no ground-truth labels for "anomalous" days, so the model is sanity-checked against well-known BTC market shocks. An event counts as detected if at least one anomaly is flagged within ±3 days (`src/04_validate_events.py`).

| Event | Date | Detected | Severity | Top Driver |
|---|---|---|---|---|
| Early-2015 crash | 2015-01-14 | ✅ | High | log_return |
| 2017 bubble peak | 2017-12-17 | ✅ | Low | volatility_14 |
| Nov 2018 sell-off | 2018-11-20 | ✅ | Medium | log_return |
| COVID-19 crash | 2020-03-12 | ✅ | High | log_return |
| China mining crackdown | 2021-05-19 | ✅ | High | log_return |
| Terra/LUNA collapse | 2022-05-09 | ✅ | Medium | log_return |
| Celsius / 3AC contagion | 2022-06-13 | ✅ | High | log_return |
| FTX collapse | 2022-11-08 | ✅ | Medium | log_return |
| Aug 2024 global sell-off | 2024-08-05 | ❌ | – | – |

**Result: 8/9 events detected.** For reference, with a 3% anomaly rate a random flagger would hit a given 7-day window only ~19% of the time (1 − 0.97⁷).

---

## Tools & Technologies
- **Python:** pandas, numpy, scikit-learn
- **Machine Learning:** Isolation Forest
- **Visualization:** Tableau Public
- **Version Control:** Git & GitHub

---

## Key Takeaways
- Unsupervised learning can effectively monitor volatile systems without labeled data
- Feature engineering is critical for meaningful anomaly detection
- Dashboards are essential for translating model output into actionable insight
- Explainability needs care: driver attribution must use standardized features, otherwise large-scale features dominate

---

## Limitations & Next Steps
- **Retrospective, not real-time:** the scaler and Isolation Forest are fit on the full history, so each day is scored with knowledge of later data. A true early-warning setup would refit on an expanding window and score only the next day (walk-forward).
- **Fixed contamination (3%):** the anomaly rate is a chosen parameter, not learned from data.
- **Single asset:** extending to multiple assets or on-chain metrics would test generalization.

---

## Disclaimer
This project is for **educational and portfolio purposes only**.  
It is not financial advice and does not constitute a trading system.

