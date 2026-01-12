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
    └── 03_anomaly_detection.py
```

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
- Finance-leaning data can be framed for **general data, tech, and fintech roles**

---

## Disclaimer
This project is for **educational and portfolio purposes only**.  
It is not financial advice and does not constitute a trading system.

