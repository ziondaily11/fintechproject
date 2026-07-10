# FINPULSE 💸🔍
### Mobile Money Fraud Analytics Dashboard

FinPulse is an interactive dashboard that analyzes 120,000 mobile money transactions to surface fraud patterns, flag high-risk segments, and generate dynamic, plain-language findings and recommendations. Built as my first end-to-end data analytics project — from raw data, to a modular codebase, to a deployed, interactive app.

> 🔗 **LINK** [https://finpulse-kenya.streamlit.app]
> ## Dataset

This project uses the [M-Pesa Transactions Fraud Detection](https://www.kaggle.com/datasets/calebboen/mpesa-transactions-fraud) dataset from Kaggle, created by Caleb Boen. It contains 120,000 synthetic mobile money transfer records modeled on Kenya's M-Pesa platform, including transaction type (TILL, PEER, PAYBILL), amount, region, hour, device type, and a binary `is_fraud` label. Because the data is synthetic rather than sourced from real customer transactions, it's well suited for practicing fraud analytics and dashboard-building without any privacy concerns — but findings shouldn't be read as claims about real-world M-Pesa fraud rates.

---

## Overview

Mobile money platforms (TILL, PEER-to-peer, and PAYBILL transactions) process huge volumes daily, and fraud tends to hide in specific segments — certain hours, regions, transaction sizes, or device types. FinPulse lets you slice 120K transactions by region, transaction type, fraud status, and hour to answer: **where, when, and how is fraud happening?**

Every KPI, chart, and written insight on the dashboard recalculates live based on the filters selected — nothing is hardcoded.

## Features

- **Interactive filters** — region, transaction type, fraud status, and hour, so you can drill into any segment
- **KPI summary cards** — total transactions, total volume, fraud rate, average legitimate vs. fraudulent amount, and peak fraud hour, each shown relative to the full dataset
- **Dynamic insights** — plain-language findings that adapt to the current filter selection (e.g. flagging when fraudulent transactions run significantly larger than legitimate ones, or when a selection has too few transactions to draw conclusions from)
- **Actionable recommendations** — suggested amount thresholds or time windows for manual review, generated from the filtered data rather than fixed text
- **Visual breakdowns:**
  - Amount distribution (with value labels on each bar)
  - Transaction type split (TILL / PEER / PAYBILL)
  - Fraud rate by region
  - Fraud rate by transaction amount bucket
  - Transactions vs. fraud rate by hour (dual-axis)
  - Transaction volume by day of week
  - Fraud counts by hour of day
  - Device type (smartphone vs. feature phone) fraud rate by region — computed dynamically per selection

## Key Findings (unfiltered dataset)

- **120,000** transactions totaling **KES 180.8M**, with an overall fraud rate of **2.92%** (3,510 flagged transactions)
- Fraudulent transactions average **KES 2,535** vs. **KES 1,476** for legitimate ones — fraud disproportionately targets higher-value transactions
- Fraud peaks at **9 PM** (172 cases) and **4 AM** (170 cases) — both fall within normal transacting hours, so timing alone isn't a strong standalone signal
- Device usage is nearly a **50/50 split** between smartphones and feature phones across regions

## Tech Stack

- **Python** — core language
- **Pandas** — data cleaning, aggregation, and analysis
- **Streamlit** — dashboard framework and deployment
- **Plotly** — interactive charts and visualizations

## Project Structure

This project is split into focused modules rather than one large script, to keep each piece of logic easy to find, test, and edit independently:

```
finpulse/
├── Safaricom Data Project.py       # Entry point — page config, layout, orchestrates all modules
├── data_loader.py       # Loads and cleans the dataset; all aggregations/calculations (calc())
├── filters.py            # Filter widgets (region, txn type, fraud status, hour) + filtering logic
├── kpis.py                # KPI card calculations and rendering, number/hour formatting helpers
├── charts.py               # All Plotly chart-building functions
├── insights.py              # Dynamic findings & recommendations (the blue insight boxes)
├── mpesa_synthetic.csv        # Transaction dataset
├── projectlogo.png             # Dashboard logo
└── requirements.txt
```

**How it fits together:** `Safaricom Data Project.py` loads the data once via `data_loader.py`, renders the filter bar via `filters.py`, recalculates everything for the filtered selection, then hands that filtered data off to `kpis.py`, `charts.py`, and `insights.py` to render. No module talks to Streamlit's UI except through its own render functions, which keeps each file testable on its own.

## Getting Started

### Prerequisites
- Python 3.9+

### Installation

```bash
# Clone the repository
git clone https://github.com/ziondaily11/fintechproject.git
cd finpulse

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run "Safaricom Data Project.py"
```

The app will open at `http://localhost:8501`.

## Requirements

```
streamlit
pandas
plotly
plotly_express
streamlit-option-menu
```

## Roadmap / Ideas for Next Iteration

- [ ] Add a machine learning model to predict fraud probability per transaction
- [ ] Export filtered views as CSV/PDF reports
- [ ] Add anomaly detection for real-time flagging
- [ ] User authentication for investigator-level access
- [ ] Unit tests for `data_loader.calc()` and the insight-generation functions

## About This Project

This is my first Python data analytics project, built to practice the full workflow: data cleaning with Pandas, exploratory analysis, dashboard design, dynamic insight generation, and deployment with Streamlit — including refactoring from a single large script into a modular, maintainable codebase. Feedback is welcome!

## License
## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contact
ELVIS — 1elvisdaily@gmail.com
Find me on X-https://x.com/TheeAnalyst_ke
