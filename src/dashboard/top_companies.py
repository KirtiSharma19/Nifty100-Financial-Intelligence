import streamlit as st

from src.services.ratio_engine import DatasetBuilder


def show_top_companies():

    st.title("Top Companies Dashboard")

    # ----------------------------------------
    # Load Data
    # ----------------------------------------

    engine = DatasetBuilder()

    df = engine.build_dataset()

    latest_year = df["year"].max()

    latest = df[df["year"] == latest_year].copy()

    # ----------------------------------------
    # KPI Cards
    # ----------------------------------------

    st.header("Dashboard Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Companies",
        latest["company_name"].nunique()
    )

    col2.metric(
        "Highest Quality",
        round(latest["quality_score"].max(), 2)
    )

    col3.metric(
        "Highest ROE %",
        round(latest["return_on_equity_pct"].max(), 2)
    )

    col4.metric(
        "Highest Margin %",
        round(latest["net_profit_margin_pct"].max(), 2)
    )

    st.divider()

    # ----------------------------------------
    # Top Quality Companies
    # ----------------------------------------

    st.header("Top 10 Quality Companies")

    top_quality = (
        latest[
            [
                "company_name",
                "broad_sector",
                "quality_score",
                "return_on_equity_pct",
                "net_profit_margin_pct",
            ]
        ]
        .sort_values(
            "quality_score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_quality,
        use_container_width=True
    )

    st.bar_chart(
        top_quality.set_index("company_name")[
            "quality_score"
        ]
    )

    st.divider()

    # ----------------------------------------
    # Top ROE
    # ----------------------------------------

    st.header("Top 10 ROE Companies")

    top_roe = (
        latest[
            [
                "company_name",
                "return_on_equity_pct",
            ]
        ]
        .sort_values(
            "return_on_equity_pct",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_roe,
        use_container_width=True
    )

    st.bar_chart(
        top_roe.set_index("company_name")[
            "return_on_equity_pct"
        ]
    )

    st.divider()

    # ----------------------------------------
    # Top Profit Margin
    # ----------------------------------------

    st.header("Top 10 Profit Margin Companies")

    top_margin = (
        latest[
            [
                "company_name",
                "net_profit_margin_pct",
            ]
        ]
        .sort_values(
            "net_profit_margin_pct",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_margin,
        use_container_width=True
    )

    st.bar_chart(
        top_margin.set_index("company_name")[
            "net_profit_margin_pct"
        ]
    )

    st.divider()

    # ----------------------------------------
    # Top Free Cash Flow
    # ----------------------------------------

    st.header("Top 10 Free Cash Flow Companies")

    top_cash = (
        latest[
            [
                "company_name",
                "free_cash_flow_cr",
            ]
        ]
        .sort_values(
            "free_cash_flow_cr",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_cash,
        use_container_width=True
    )

    st.bar_chart(
        top_cash.set_index("company_name")[
            "free_cash_flow_cr"
        ]
    )

    st.divider()

    # ----------------------------------------
    # Download CSV
    # ----------------------------------------

    csv = top_quality.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Top Companies",
        csv,
        file_name="top_companies.csv",
        mime="text/csv",
    )