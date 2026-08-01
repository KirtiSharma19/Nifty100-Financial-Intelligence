# 📈 Nifty100 Financial Intelligence Dashboard

A complete Financial Intelligence Dashboard built using Python, Pandas and Streamlit for analysing Nifty 100 companies.

---

# Features

- Company Dashboard
- Sector Dashboard
- KPI Dashboard
- Top Companies Dashboard
- Financial Ratio Analysis
- Quality Score Calculation
- CAGR Analysis
- Cash Flow Analysis
- Valuation Analysis
- CSV Report Export
- Interactive Charts

---

# Tech Stack

- Python
- Pandas
- NumPy
- Streamlit
- Matplotlib
- SQLite

---

# Folder Structure

```
src/
    analytics/
    dashboard/
    services/
    reports/
    utils/
    config/
    etl/
    models/
    screener/

exports/
    charts/
    radar_charts/
    reports/

data/
database/
```

---

# Financial KPIs

- Return on Equity
- Net Profit Margin
- Operating Profit Margin
- Debt to Equity
- Free Cash Flow
- CAPEX
- Market Capitalization
- Enterprise Value
- PE Ratio
- PB Ratio
- EV/EBITDA
- Dividend Yield

---

# Dashboards

## Home Dashboard

Overall Financial Summary with key financial KPIs, sector overview and top-performing companies.

## Company Profile Dashboard

Detailed company profile with financial metrics, historical trends and performance analysis.

## Financial Screener Dashboard

Filter companies using financial ratios, quality score and sector-wise screening with CSV export.

## Peer Comparison Dashboard

Compare a company with its industry peers using radar charts, KPI comparison tables and visual analytics.

## Trend Analysis Dashboard

Analyze 10-year financial trends with interactive charts and multi-metric comparison.

## Sector Analysis Dashboard

Compare sectors using bubble charts, sector KPIs and performance distribution.

## Capital Allocation Dashboard

Visualize capital allocation patterns across companies with treemap and allocation insights.

## Reports Dashboard

Generate and download financial reports, valuation reports and annual report links.

---

# Generated Reports

- final_financial_report.csv
- sector_report.csv
- valuation_report.csv
- cashflow_report.csv
- cagr_report.csv
- valuation_report.csv
- financial_report.csv
- peer_comparison.csv
- peer_comparison.xlsx
- screener_output.csv

---

# Charts

- Sector Quality
- Valuation
- CAGR
- Cash Flow
- Top Quality Companies

---

# Run Project

```bash
pip install -r requirements.txt

streamlit run src/dashboard/app.py
```
---