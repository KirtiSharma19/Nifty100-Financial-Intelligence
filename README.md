# 📈 NIFTY100 Financial Intelligence

A comprehensive financial intelligence platform for analysing NIFTY 100 companies using financial ratios, profitability metrics, growth indicators, cash-flow KPIs, valuation metrics, quality scores, peer comparison and sector-level analysis.

The project combines **Python-based financial analytics, data processing, Streamlit dashboards and REST APIs** to provide an end-to-end financial analysis system.

---

## 🚀 Features

### 📊 Financial Analysis
- Financial ratio analysis
- Profitability analysis
- Return on Equity (ROE)
- Net Profit Margin
- Operating Profit Margin
- Debt-to-Equity analysis
- Free Cash Flow analysis
- CAPEX analysis
- Cash Flow KPIs

### 📈 Growth Analysis
- Revenue CAGR
- Profit CAGR
- Free Cash Flow CAGR
- Historical financial trends
- Top-performing companies based on growth metrics

### 💰 Valuation Analysis
- Market Capitalization
- Enterprise Value
- PE Ratio
- PB Ratio
- EV/EBITDA
- Dividend Yield
- Valuation comparison

### 🏆 Company Scoring
- Quality Score
- Composite Score
- Company ranking
- Financial performance comparison

### 🏢 Sector Analysis
- Sector-wise company count
- Average and median ROE
- Average Debt-to-Equity
- Revenue CAGR comparison
- FCF CAGR comparison
- Operating margin comparison
- Quality score comparison
- Composite score comparison

### 🔍 Financial Screener
Filter companies using multiple financial parameters such as:

- ROE
- Debt-to-Equity
- Free Cash Flow
- Sector
- Revenue CAGR
- Profit CAGR
- PE Ratio
- Other financial metrics

The screener also supports ranked company results and CSV export.

### 🤝 Peer Comparison
- Compare companies with their peers
- Financial KPI comparison
- Radar chart analysis
- Peer comparison reports

### 💼 Portfolio Analysis
- Portfolio-level financial analysis
- Company allocation insights
- Financial performance comparison

### 📄 Reports & Documents
- Financial reports
- Valuation reports
- Sector reports
- CAGR reports
- Cash-flow reports
- Peer comparison reports
- CSV/XLSX exports
- Annual report/document links

---

# 🖥️ Dashboards

## 🏠 Home Dashboard

Provides an overall financial summary including:

- Key financial KPIs
- Sector overview
- Top-performing companies
- Financial highlights

---

## 🏢 Company Profile Dashboard

Provides detailed company-level analysis including:

- Company information
- Financial metrics
- Historical performance
- Financial ratios
- Growth indicators
- Valuation metrics

---

## 🔎 Financial Screener Dashboard

Allows users to filter and rank NIFTY 100 companies based on financial metrics.

Example filters include:

- Minimum ROE
- Maximum Debt-to-Equity
- Minimum Free Cash Flow
- Sector
- Minimum Revenue CAGR
- Minimum Profit CAGR
- Maximum PE Ratio

Results can be exported as CSV.

---

## 🤝 Peer Comparison Dashboard

Compare a company against its peers using:

- KPI comparison tables
- Financial ratios
- Growth metrics
- Quality scores
- Composite scores
- Radar charts

---

## 📈 Trend Analysis Dashboard

Analyse historical financial performance using:

- Revenue trends
- Profitability trends
- Cash-flow trends
- Ratio trends
- Multi-year comparisons

---

## 🏭 Sector Analysis Dashboard

Compare sectors using:

- Company count
- ROE
- Debt-to-Equity
- Revenue CAGR
- FCF CAGR
- Operating margin
- Quality score
- Composite score

---

## 💼 Capital Allocation Dashboard

Visualise capital allocation patterns and analyse how companies allocate capital across different financial activities.

---

## 📑 Reports Dashboard

Generate and access financial reports including:

- Financial reports
- Sector reports
- Valuation reports
- CAGR reports
- Cash-flow reports
- Peer comparison reports
- Exportable datasets

---

# 🔌 REST API

The project also provides a **FastAPI REST API** for accessing financial intelligence programmatically.

### API Base URL

```text
/api/v1

## 🔗 Quick Links

| Resource | Link |
|---|---|
| 📦 Repository | [Open Repository](.) |
| 📊 Streamlit Dashboard | [Dashboard Source](src/dashboard/app.py) |
| 🔌 FastAPI Application | [API Source](src/api/main.py) |
| 🏭 Sector API | [Sectors API](src/api/routers/sectors.py) |
| 🔎 Screener API | [Screener API](src/api/routers/screener.py) |
| 🏢 Companies API | [Companies API](src/api/routers/companies.py) |
| 👥 Peer API | [Peers API](src/api/routers/peers.py) |
| 💰 Valuation API | [Valuation API](src/api/routers/valuation.py) |
| 💼 Portfolio API | [Portfolio API](src/api/routers/portfolio.py) |
| 📄 Documents API | [Documents API](src/api/routers/documents.py) |
| 🧮 Ratio Engine | [Ratio Engine](src/services/ratio_engine.py) |
| 📈 Ratio Analytics | [Ratios](src/analytics/ratios.py) |
| 📈 CAGR Analysis | [CAGR](src/analytics/cagr.py) |
| 💵 Cash Flow Analysis | [Cash Flow Intelligence](src/analytics/cashflow_intelligence.py) |
| ⭐ Company Scoring | [Company Score](src/analytics/company_score.py) |
| 🏆 Composite Scoring | [Composite Score](src/analytics/composite_score.py) |
| 👥 Peer Analysis | [Peer Analysis](src/analytics/peer.py) |
| 🏭 Clustering | [Clustering](src/analytics/clustering.py) |
| 📊 Radar Charts | [Radar Charts](src/analytics/radar_chart.py) |
| 💰 Valuation Analysis | [Valuation](src/analytics/valuation.py) |
| 🧪 Tests | [Tests Folder](tests/) |
| 📁 Reports | [Reports](reports/) |
| 📤 Exports | [Exports](exports/) |
| ⚙️ Requirements | [requirements.txt](requirements.txt) |

---
## 🔗 Quick Links

| Resource | Link |
|---|---|
| 📦 Repository | [Open Repository](.) |
| 📊 Streamlit Dashboard | [Dashboard Source](src/dashboard/app.py) |
| 🔌 FastAPI Application | [API Source](src/api/main.py) |
| 🏭 Sector API | [Sectors API](src/api/routers/sectors.py) |
| 🔎 Screener API | [Screener API](src/api/routers/screener.py) |
| 🏢 Companies API | [Companies API](src/api/routers/companies.py) |
| 👥 Peer API | [Peers API](src/api/routers/peers.py) |
| 💰 Valuation API | [Valuation API](src/api/routers/valuation.py) |
| 💼 Portfolio API | [Portfolio API](src/api/routers/portfolio.py) |
| 📄 Documents API | [Documents API](src/api/routers/documents.py) |
| 🧮 Ratio Engine | [Ratio Engine](src/services/ratio_engine.py) |
| 📈 Ratio Analytics | [Ratios](src/analytics/ratios.py) |
| 📈 CAGR Analysis | [CAGR](src/analytics/cagr.py) |
| 💵 Cash Flow Analysis | [Cash Flow Intelligence](src/analytics/cashflow_intelligence.py) |
| ⭐ Company Scoring | [Company Score](src/analytics/company_score.py) |
| 🏆 Composite Scoring | [Composite Score](src/analytics/composite_score.py) |
| 👥 Peer Analysis | [Peer Analysis](src/analytics/peer.py) |
| 🏭 Clustering | [Clustering](src/analytics/clustering.py) |
| 📊 Radar Charts | [Radar Charts](src/analytics/radar_chart.py) |
| 💰 Valuation Analysis | [Valuation](src/analytics/valuation.py) |
| 🧪 Tests | [Tests Folder](tests/) |
| 📁 Reports | [Reports](reports/) |
| 📤 Exports | [Exports](exports/) |
| ⚙️ Requirements | [requirements.txt](requirements.txt) |

---
                    ┌─────────────────────────┐
                    │    Raw Financial Data   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       ETL / Cleaning    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Dataset Builder     │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌────────────┐     ┌────────────┐     ┌────────────┐
       │ Financial  │     │    CAGR    │     │ Cash Flow  │
       │   Ratios   │     │  Analysis  │     │  Analysis  │
       └──────┬─────┘     └──────┬─────┘     └──────┬─────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │ Quality / Composite     │
                    │        Scoring           │
                    └────────────┬────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼
      ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
      │  Streamlit  │     │   FastAPI   │     │   Reports   │
      │  Dashboard  │     │     API     │     │ CSV / Excel │
      └─────────────┘     └─────────────┘     └─────────────┘

NIFTY100-Financial-Intelligence/
│
├── data/
│
├── database/
│
├── exports/
│   ├── charts/
│   ├── radar_charts/
│   ├── reports/
│   ├── peer_comparison.csv
│   ├── peer_comparison.xlsx
│   └── screener_output.csv
│
├── reports/
│   ├── portfolio/
│   ├── sector/
│   └── tearsheets/
│
├── src/
│   │
│   ├── analytics/
│   │   ├── cagr.py
│   │   ├── cashflow_intelligence.py
│   │   ├── cashflow_kpis.py
│   │   ├── cluster_statistics.py
│   │   ├── clustering.py
│   │   ├── company_score.py
│   │   ├── composite_score.py
│   │   ├── peer.py
│   │   ├── radar_chart.py
│   │   ├── ratios.py
│   │   └── valuation.py
│   │
│   ├── api/
│   │   ├── main.py
│   │   └── routers/
│   │       ├── companies.py
│   │       ├── documents.py
│   │       ├── peers.py
│   │       ├── portfolio.py
│   │       ├── screener.py
│   │       ├── sectors.py
│   │       └── valuation.py
│   │
│   ├── config/
│   │
│   ├── dashboard/
│   │   └── app.py
│   │
│   ├── etl/
│   │
│   ├── models/
│   │
│   ├── nlp/
│   │
│   ├── reports/
│   │
│   ├── screener/
│   │
│   ├── services/
│   │   └── ratio_engine.py
│   │
│   └── utils/
│
├── tests/
│   ├── api/
│   ├── etl/
│   ├── kpi/
│   └── ...
│
├── requirements.txt
├── pytest.ini
└── README.md

--- Run Dashboard
streamlit run src/dashboard/app.py
The dashboard will normally open at:

http://localhost:8501

⚡ Quick Start
For Windows:

git clone <YOUR-GITHUB-REPOSITORY-URL>

cd NIFTY100-Financial-Intelligence

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

python -m pytest -q

streamlit run src/dashboard/app.py
Then open:

http://localhost:8501
For API:

uvicorn src.api.main:app --reload
Then open:

http://127.0.0.1:8000/docs