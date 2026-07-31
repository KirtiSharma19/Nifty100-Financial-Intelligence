import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from src.dashboard.top_companies import show_top_companies
from src.dashboard.company_dashboard import show_company_dashboard
from src.services.ratio_engine import DatasetBuilder
import plotly.express as px
from src.dashboard.sector_dashboard import show_sector_dashboard
from src.dashboard.kpi_dashboard import show_kpi_dashboard

st.set_page_config(
    page_title="Nifty100 Financial Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Nifty100 Financial Intelligence")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Home",
        "Company Dashboard",
        "Top Companies",
        "Sector Dashboard",
        "KPI Dashboard"
    ]
)

if page == "Home":

    engine = DatasetBuilder()
    df = engine.build_dataset()

    df["year_dt"] = pd.to_datetime(df["year"], errors="coerce")

    latest = (
        df
        .sort_values("year_dt")
        .groupby("company_name", as_index=False)
        .tail(1)
    )

    st.header("📊 Dashboard Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Companies",
        latest["company_name"].nunique()
    )

    col2.metric(
        "Average Quality",
        round(latest["quality_score"].mean(), 2)
    )

    col3.metric(
        "Average ROE",
        round(latest["return_on_equity_pct"].mean(), 2)
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Average Margin",
        round(latest["net_profit_margin_pct"].mean(), 2)
    )

    col5.metric(
        "Average Debt/Equity",
        round(latest["debt_to_equity"].mean(), 2)
    )

    col6.metric(
        "Sectors",
        latest["broad_sector"].nunique()
    )

    sector = (
        latest
        .groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector,
        names="broad_sector",
        values="Companies",
        title="Sector Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("🏆 Top 5 Companies")

    top5 = latest.sort_values(
        "quality_score",
        ascending=False
    ).head(5)

    st.dataframe(
        top5[
        [
            "company_name",
            "broad_sector",
            "quality_score",
            "return_on_equity_pct",
        ]
        ],
        use_container_width=True
    )
    st.write("Total Rows :", len(df))
    st.write("Unique Companies :", df["company_name"].nunique())
    st.write("Latest Year :", latest)
    st.write("Rows in Latest :", len(latest))
    st.write(latest.head())

elif page == "Company Dashboard":
    show_company_dashboard()

elif page == "Top Companies":
    show_top_companies()

elif page == "Sector Dashboard":
    show_sector_dashboard()

elif page == "KPI Dashboard":
    show_kpi_dashboard()