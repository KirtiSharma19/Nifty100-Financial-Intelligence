import streamlit as st
import pandas as pd

from src.services.ratio_engine import DatasetBuilder


def show():

    st.title("Stock Screener")

    engine = DatasetBuilder()

    df = engine.build_dataset()

    years = sorted(df["year"].unique())

    year = st.sidebar.selectbox(
        "Year",
        years,
        index=len(years)-1
    )

    data = df[df["year"] == year]

    st.sidebar.header("Filters")

    roe_min = st.sidebar.slider(
        "Minimum ROE",
        0.0,
        50.0,
        15.0
    )

    debt_max = st.sidebar.slider(
        "Maximum Debt/Equity",
        0.0,
        5.0,
        1.0
    )

    margin_min = st.sidebar.slider(
        "Minimum Net Margin",
        0.0,
        50.0,
        10.0
    )

    pe_max = st.sidebar.slider(
        "Maximum PE",
        0.0,
        100.0,
        40.0
    )

    quality_min = st.sidebar.slider(
        "Minimum Quality Score",
        0,
        100,
        60
    )

    sector = st.sidebar.selectbox(
        "Sector",
        ["All"] + sorted(data["broad_sector"].dropna().unique().tolist())
    )

    filtered = data.copy()

    filtered = filtered[
        filtered["return_on_equity_pct"] >= roe_min
    ]

    filtered = filtered[
        filtered["debt_to_equity"] <= debt_max
    ]

    filtered = filtered[
        filtered["net_profit_margin_pct"] >= margin_min
    ]

    filtered = filtered[
        filtered["pe_ratio"] <= pe_max
    ]

    filtered = filtered[
        filtered["quality_score"] >= quality_min
    ]

    if sector != "All":

        filtered = filtered[
            filtered["broad_sector"] == sector
        ]

    filtered = filtered.sort_values(
        "composite_score",
        ascending=False
    )

    st.subheader(
        f"Companies Found : {len(filtered)}"
    )

    show_cols = [

        "company_name",
        "broad_sector",
        "quality_score",
        "composite_score",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "pe_ratio",
        "pb_ratio",
        "market_cap_crore"

    ]

    st.dataframe(

        filtered[show_cols],

        use_container_width=True

    )

    csv = filtered[show_cols].to_csv(index=False)

    st.download_button(

        "Download CSV",

        csv,

        file_name="screener_output.csv",

        mime="text/csv"

    )